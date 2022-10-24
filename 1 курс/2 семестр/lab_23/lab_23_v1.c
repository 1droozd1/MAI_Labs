#include <stdio.h> 
#include <stdlib.h>

struct tnode 
{
  int field;           // поле данных
  int dep;           // глубина дерева
  struct tnode *left;  // левый потомок
  struct tnode *right; // правый потомок
};

struct tnode *addnode(struct tnode *tree, int x, int depth_loc) {
    depth_loc ++;
  if (tree == NULL) { // Случай, когда дерева нет - формирование корня дерева
    struct tnode *tree = malloc(sizeof(struct tnode)); // память под узел
    tree->field = x;   // поле данных
    tree->dep = depth_loc;
    tree->left =  NULL;
    tree->right = NULL; // ветви инициализируем пустотой
    return tree;
  }
  if (x < tree->field) {
    tree->left = addnode(tree->left, x, depth_loc);
  }
  if (x > tree->field) {
    tree->right = addnode(tree->right, x, depth_loc);
  }
  return(tree);
}

struct tnode *infimum(struct tnode *tree)
{
    if (tree->left == NULL)
        return tree;
    return infimum(tree->left);
}

struct tnode *delete(struct tnode *tree, int field) {
    if (tree == NULL) {
        return tree;
    }
    if (field < tree->field) {
        tree->left = delete(tree->left, field);
    } else if (field > tree ->field) {
        tree->right = delete(tree->right, field);
    } else if (tree->left != NULL && tree->right != NULL) {
        tree->field = infimum(tree->right)->field;
        tree->right = delete(tree->right, tree->field);
    }
    else if (tree->left != NULL) 
    {
        struct tnode *left = tree->left;
        free(tree);
        tree = left;
    }
    else if (tree->right != NULL) 
    {
        struct tnode *right = tree->right;
        free(tree);
        tree = right;
    }
    else 
    {
        free(tree);
        tree = NULL;
    }
    return tree;
}

int search(struct tnode *tree, int number) 
{
    if (tree == NULL) 
        return 0;
    if (number == tree->field) {
        return 1;
    }
    if (number < tree->field && tree->left != NULL) {
        return search(tree->left, number);
    }
    if (number > tree->field && tree->right != NULL) { 
        return search(tree->right, number);
    } else {
        return 0;
    }
}

void preorder(struct tnode *tree) // прямой тип обхода
{
    if (tree == NULL)
        return;
    printf("(");
    printf("%d ", tree->field);
    preorder(tree->left);
    preorder(tree->right);
    printf(")");
}

void postorder(struct tnode *tree) // обратный тип одхода
{
    if (tree == NULL) 
        return;
    preorder(tree->left);
    preorder(tree->right);
    printf("%d ", tree->field);
}

void inorder(struct tnode *tree) // центрированный тип обхода
{
    if (tree == NULL) 
        return;
    inorder(tree->left);
    printf("%d ", tree->field);
    inorder(tree->right);
}

int depth(struct tnode *tree, int m) //определение высоты дерева
{
    if (tree == NULL)
        return m;
    if (tree->dep > m)
        m = tree->dep;
    depth(tree->left, m);
    depth(tree->right, m);
}

int width(struct tnode *tree, int depth_loc, int *arr, int result)
{
    if (tree == NULL)
    {
        for (int i = 0; i <= depth_loc; i++)
        {
            if (arr[i] > result)
                result = arr[i];
        }
        return result;
    }
    width(tree->left, depth_loc, arr, result);
    arr[tree->dep] ++; /*причем dep - структурный */
    width(tree->right, depth_loc, arr, result);
}

void freememory(struct tnode *tree) {
  if(tree!=NULL) {
    freememory(tree->left);
    freememory(tree->right);
    free(tree);
  }
}

int main(void)
{
    printf("Possible operations:\n");
    printf("an --- add element n to the tree\n");
    printf("$ --- end of adding elements\n");
    printf("rn --- remove element n from the tree\n");
    printf("sn --- search element n in the tree\n");
    printf("p1 --- output the tree by preorder\n");
    printf("p2 --- output the tree by postorder\n");
    printf("p3 --- outout the tree by inorder\n");
    printf("# --- finish\n");
    int value;
    char word;
    struct tnode *tree = NULL;
    
    scanf("%c %d", &word, &value);
    tree = addnode(tree, value, 1); /*где 1 - текущая глубина*/
    while (word != '$')
    {
        scanf("%c", &word);
        if (word == 'a') {
            scanf("%d", &value);
            tree = addnode(tree, value, 1);
        }
    }

    int array[129];
    int dep = depth(tree, 0);
    for (int i = 0; i < 129; i++) {
        array[i] = 0;
    }
    int i_max = 0;
    int result = width(tree, dep, array, 0);
    for (int i = 0; i < 129; i++) {
        if (array[i] == result) {
            i_max = i;
            break;
        }
    }
    printf("Tree level with maximum number of tops is %d\n", i_max);

    /*printf("\nPrint 'help' to check all information about programm\n\n");*/

    scanf("%c", &word);
    while (word != '#') {
        scanf("%c", &word);
        if (word == 'r') {
            scanf("%d", &value);
            tree = delete(tree, value);
        }
        if (word == 'p') {
            scanf("%d", &value);
            if (value == 1) {
                preorder(tree);
            } else if (value == 2) {
                postorder(tree);
            } else {
                inorder(tree);
            }
            printf("\n");
        }
        if (word == 's') {
            scanf("%d", &value);
            if (search(tree, value) == 1) {
                printf("True");
            } else {
                printf("False");
            }
        }
    }
    freememory(tree);
    return 0;
}