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
void inorder(struct tnode *tree) // центрированный тип обхода
{
    if (tree == NULL) 
        return;
    inorder(tree->left);
    printf("%d ", tree->field);
    inorder(tree->right);
}

struct tnode *rem(struct tnode *tree)
{
    if (tree == NULL) 
        return tree;
    if (tree->left == NULL && tree->right == NULL)
    {
        free(tree);
        return NULL;
    }
    if (tree->right != NULL)
        tree->right = rem(tree->right);
    if (tree->left != NULL)
        tree->left = rem(tree->left);
    return rem(tree);
}

int main()
{
    struct node* T = NULL;
    int p = 0;
    char c = 'a';
    do
    {
        int n = 0;
        int rn = 0;
        int rd = 0;
        char f;
        scanf("%c", &c);
        if (c != '(')
        {
            f = c;
        }
        if (c == '(')
        {
            scanf("%c", &c);
            scanf("%c", &c);
            f = c;
            rd++;
        }
        if (c == '-')
        {
            scanf("%c", &c);
            f = c;
            rd++;
        }
        while ((c >= '0')&&(c <= '9'))
        {
            n *= 10;
            n += c - '0';
            scanf("%c", &c);
        }
        int g = 0;
        g = n;
        n = 0; 
        while ((c != '+')&&(c != '/')&&(c != '\n')&&(c != '-'))
        {
            scanf("%c", &c);
            while ((c >= '0')&&(c <= '9'))
            {
                n *= 10;
                n += c - '0';
                scanf("%c", &c);
                rn++;
            }
            if (rn != 0)
            {
                T = add(T, n, '^');
                rn = 0;
                n = 0;
            }
            if ((c >= 'a')&&(c <= 'z'))
                T = add(T, 0, c);
            if (c == '(')
            {
                rd++;
                scanf("%c", &c);
                c = 'a';
            } 
        }
        if ((rd % 2 == 0)&&(g == 0)&&(p == 0))
        {
            printf("%c", f);
            inorder(T);
        }
        if ((rd % 2 == 0)&&(g == 0)&&(p > 0))
        {
            printf("%c", f);
            inorder(T);
        }
        if ((rd % 2 == 0)&&(g != 0)&&(p == 0))
        {
            printf("%d", g);
            inorder(T);
        }
        if ((rd % 2 == 0)&&(g != 0)&&(p > 0))
        {
            printf("%d", g);
            inorder(T);
        }
        if ((rd % 2 == 1)&&(g == 0)&&(p == 0))
        {
            printf("-%c", f);
            inorder(T);            
        }
        if ((rd % 2 == 1)&&(g == 0)&&(p > 0))
        {
            printf("(-%c", f);
            inorder(T);
            printf(")");
        }
        if ((rd % 2 == 1)&&(g != 0)&&(p == 0))
        {
            printf("-%d", g);
            inorder(T);
        }
        if ((rd % 2 == 1)&&(g != 0)&&(p > 0))
        {
            printf("(-%d", g);
            inorder(T);
            printf(")");
        }
        T = rem(T);
        printf("%c", c);
        p++;
    } while (c != '\n');
    T = rem(T);
    if (c != '\n')
        printf("\n");
    return 0;
}