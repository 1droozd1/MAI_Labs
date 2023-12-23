#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

using namespace std;

vector<string> resultSequence;

// Функция для вычисления LCS для двух половин
vector<int> calculateLCS(const vector<string>& seq1, const vector<string>& seq2, int start1, int end1, int start2, int end2) {
    int len2 = end2 - start2 + 1;
    vector<int> current(len2 + 1), previous(len2 + 1);

    for (int i = start1; i <= end1; i++) {
        previous = current;
        for (int j = start2; j <= end2; j++) {
            if (seq1[i] == seq2[j]) {
                current[j - start2 + 1] = previous[j - start2] + 1;
            } else {
                current[j - start2 + 1] = max(current[j - start2], previous[j - start2 + 1]);
            }
        }
    }
    return current;
}

// Рекурсивная функция для выполнения алгоритма Хиршберга
void hirschberg(const vector<string>& seq1, const vector<string>& seq2,
                const vector<string>& revSeq1, const vector<string>& revSeq2,
                int start1, int end1, int start2, int end2) {

    // Базовые случаи
    if (end2 - start2 + 1 <= 0 || end1 < start1) {
        return;
    }

    if (end1 == start1) {
        auto it = find(seq2.begin() + start2, seq2.begin() + end2 + 1, seq1[start1]);
        if (it != seq2.end()) {
            resultSequence.push_back(seq1[start1]);
        }
        return;
    }

    int mid = ((end1 - start1 + 1) / 2) + start1 - 1;
    vector<int> firstHalfLCS = calculateLCS(seq1, seq2, start1, mid, start2, end2);
    vector<int> secondHalfLCS = calculateLCS(revSeq1, revSeq2,
                                             seq1.size() - end1 - 1, seq1.size() - mid - 2,
                                             seq2.size() - end2 - 1, seq2.size() - start2 - 1);

    int maxLCSValue = secondHalfLCS[0] + secondHalfLCS[secondHalfLCS.size() - 1];
    int splitPoint = 0;

    // Находим точку разделения, максимизирующую длину LCS
    for (int j = 0; j < end2 - start2 + 1; j++) {
        if (firstHalfLCS[j + 1] + secondHalfLCS[end2 - start2 + 1 - j] > maxLCSValue) {
            maxLCSValue = firstHalfLCS[j + 1] + secondHalfLCS[end2 - start2 + 1 - j];
            splitPoint = j + 1;
        }
    }

    if (firstHalfLCS[firstHalfLCS.size() - 1] > maxLCSValue) {
        splitPoint = end2 - start2 + 1;
    }
    splitPoint--;

    // Рекурсивные вызовы для двух половин
    hirschberg(seq1, seq2, revSeq1, revSeq2, start1, mid, start2, splitPoint + start2);
    hirschberg(seq1, seq2, revSeq1, revSeq2, mid + 1, end1, splitPoint + start2 + 1, end2);
}

// Рекурсивная функция для обработки случая, когда первая последовательность короче
void reverseHirschberg(const vector<string>& seq1, const vector<string>& seq2,
                       const vector<string>& revSeq1, const vector<string>& revSeq2,
                       int start1, int end1, int start2, int end2) {
    if (end1 - start1 < end2 - start2) {
        hirschberg(seq1, seq2, revSeq1, revSeq2, start1, end1, start2, end2);
    } else {
        hirschberg(seq2, seq1, revSeq2, revSeq1, start2, end2, start1, end1);
    }
}

int main() {
    vector<string> sequence1, sequence2, revSequence1, revSequence2;

    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    string line1, line2;
    getline(cin, line1);
    getline(cin, line2);

    istringstream iss1(line1), iss2(line2);

    string word;
    while (iss1 >> word) {
        sequence1.push_back(word);
        revSequence1.push_back(word);
    }

    while (iss2 >> word) {
        sequence2.push_back(word);
        revSequence2.push_back(word);
    }

    reverse(revSequence1.begin(), revSequence1.end());
    reverse(revSequence2.begin(), revSequence2.end());

    reverseHirschberg(sequence1, sequence2, revSequence1, revSequence2, 0, sequence1.size() - 1, 0, sequence2.size() - 1);
    
    cout << resultSequence.size() << '\n';
    for (const auto& word : resultSequence) {
        cout << word << " ";
    }
    cout << '\n';

    return 0;
}
