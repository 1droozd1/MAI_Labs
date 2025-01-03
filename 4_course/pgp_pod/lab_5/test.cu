#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

#define SHARED_MEMORY_MAX_SIZE 1024
#define UINT_SIZE 32

#define ERROR_HANDLING(call) { \
    cudaError error = call; \
    if (error != cudaSuccess) { \
        fprintf(stderr, "ERROR: file '%s' in line %d: %s.\n", __FILE__, __LINE__, cudaGetErrorString(error)); \
        exit(1); \
    } \
}

// Функция для вывода массива (для отладки)
void print_array(uint *a, int n) {
    for (int i = 0; i < n; i++)
        printf("%u ", a[i]);
    printf("\n");
}

// Устройство: Сканирование (префиксная сумма) для одного блока
__global__
void scan_block(int *input, int *output, int n) {
    extern __shared__ int temp[];

    int th_id = threadIdx.x;
    int offset = 1;

    int left_idx = 2 * th_id;
    int right_idx = 2 * th_id + 1;

    if (left_idx < n) temp[left_idx] = input[left_idx];
    else temp[left_idx] = 0;

    if (right_idx < n) temp[right_idx] = input[right_idx];
    else temp[right_idx] = 0;

    // Построение верхнего уровня дерева
    for (int d = n >> 1; d > 0; d >>= 1) {
        __syncthreads();
        if (th_id < d) {
            int ai = offset * (2 * th_id + 1) - 1;
            int bi = offset * (2 * th_id + 2) - 1;
            temp[bi] += temp[ai];
        }
        offset <<= 1;
    }

    // Установка корня в 0
    if (th_id == 0)
        temp[n - 1] = 0;

    // Префиксная сумма
    for (int d = 1; d < n; d <<= 1) {
        offset >>= 1;
        __syncthreads();
        if (th_id < d) {
            int ai = offset * (2 * th_id + 1) - 1;
            int bi = offset * (2 * th_id + 2) - 1;
            int t = temp[ai];
            temp[ai] = temp[bi];
            temp[bi] += t;
        }
    }
    __syncthreads();

    if (left_idx < n) output[left_idx] = temp[left_idx];
    if (right_idx < n) output[right_idx] = temp[right_idx];
}

// Устройство: Получение разряда числа
__global__
void extract_bit(uint *input, int *bit_array, int digit, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        bit_array[idx] = (input[idx] >> digit) & 1;
    }
}

// Устройство: Перестановка элементов на основе битов
__global__
void rearrange(uint *output, uint *input, int *prefix_sums, int *bits, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        int pos = (bits[idx] == 0) ? idx - prefix_sums[idx] : prefix_sums[idx] + (n - prefix_sums[n - 1]);
        if (pos >= 0 && pos < n) {
            output[pos] = input[idx];
        }
    }
}

// Хост: Полная поразрядная сортировка
void radix_sort(uint *array, int n) {
    uint *d_input, *d_output;
    int *d_bits, *d_prefix_sums;

    ERROR_HANDLING(cudaMalloc(&d_input, n * sizeof(uint)));
    ERROR_HANDLING(cudaMalloc(&d_output, n * sizeof(uint)));
    ERROR_HANDLING(cudaMalloc(&d_bits, n * sizeof(int)));
    ERROR_HANDLING(cudaMalloc(&d_prefix_sums, n * sizeof(int)));

    ERROR_HANDLING(cudaMemcpy(d_input, array, n * sizeof(uint), cudaMemcpyHostToDevice));

    for (int digit = 0; digit < UINT_SIZE; digit++) {
        // Извлечение разряда
        extract_bit<<<(n + 255) / 256, 256>>>(d_input, d_bits, digit, n);

        // Префиксная сумма
        int shared_memory_size = (n > SHARED_MEMORY_MAX_SIZE) ? SHARED_MEMORY_MAX_SIZE : n;
        scan_block<<<1, shared_memory_size / 2, shared_memory_size * sizeof(int)>>>(d_bits, d_prefix_sums, n);

        // Перестановка элементов
        rearrange<<<(n + 255) / 256, 256>>>(d_output, d_input, d_prefix_sums, d_bits, n);

        // Обновление массивов
        uint *temp = d_input;
        d_input = d_output;
        d_output = temp;
    }

    ERROR_HANDLING(cudaMemcpy(array, d_input, n * sizeof(uint), cudaMemcpyDeviceToHost));

    cudaFree(d_input);
    cudaFree(d_output);
    cudaFree(d_bits);
    cudaFree(d_prefix_sums);
}

// Основная функция
int main() {
    int n;
    fread(&n, sizeof(int), 1, stdin);

    uint *array = (uint *)malloc(n * sizeof(uint));
    fread(array, sizeof(uint), n, stdin);

    radix_sort(array, n);

    fwrite(array, sizeof(uint), n, stdout);

    free(array);
    return 0;
}