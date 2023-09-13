#include <iostream>
#include <random>
#include <chrono>
#include <string.h>

using namespace std;

const size_t MAX_KEY_LEN = 280;

struct bst {
    struct node {
        node *left;
        node *right;
        char *key;
        uint64_t value;
        int y;
        node(const char *_key, uint64_t _value) {
            left = nullptr;
            right = nullptr;
            key = new char[MAX_KEY_LEN];
            memcpy(key, _key, MAX_KEY_LEN);
            value = _value;
            y = rand();
        }
        ~node() {
            delete[] key;
        }
        
    };

    using node_ptr = node *;

    node_ptr root;

    bst() {
        root = nullptr;
    }

    void destroy(node_ptr tree) {
        if (tree == nullptr) return;
        destroy(tree->left);
        destroy(tree->right);
        delete tree;
    }
    ~bst() {
        destroy(root);
    }
    node_ptr merge(node_ptr tree1, node_ptr tree2) {
        if (tree1 == nullptr) {
            return tree2;
        }
        if (tree2 == nullptr) {
            return tree1;
        }
        if (tree1->y > tree2->y) {
            tree1->right = merge(tree1->right, tree2);
            return tree1;
        } else {
            tree2->left = merge(tree1, tree2->left);
            return tree2;
        }
    }

    void split(node_ptr tree, const char *key, node_ptr& tree1, node_ptr& tree2) {
        if (tree == nullptr) {
            tree1 = nullptr;
            tree2 = nullptr;
            return;
        }
        if (strcmp(tree->key, key) < 0) {
            split(tree->right, key, tree->right, tree2);
            tree1 = tree;
        } else {
            split(tree->left, key, tree1, tree->left);
            tree2 = tree;
        }
    }

    node_ptr min_node(node_ptr ptr) {
        if (ptr == nullptr) return nullptr;
        if (ptr->left == nullptr) return ptr;
        return min_node(ptr->left);
    }

    node_ptr search(node_ptr tree, const char *key) {
        if (tree == nullptr) return nullptr;
        int rc = strcmp(tree->key, key); 
        if (rc < 0) {
            return search(tree->right, key);
        } else if (rc > 0) {
            return search(tree->left, key);
        } else {
            return tree;
        }
    }

    void find(const char *key) {
        node_ptr elem = search(root, key);
        if (elem != nullptr) {
            cout << "OK: " << elem->value << "\n";
            return;
        }
        cout << "NoSuchWord\n";
    }

    void insert(const char *key, uint64_t value) {
        node_ptr left_tree = nullptr;
        node_ptr right_tree = nullptr;
        node_ptr elem = nullptr;
        split(root, key, left_tree, right_tree);
        elem = min_node(right_tree);
        if (elem != nullptr && strcmp(elem->key, key) == 0) {
            cout << "Exist\n";
            root = merge(left_tree, right_tree);
            return;
        }
        node_ptr new_node = new node(key, value);
        root = merge(merge(left_tree, new_node), right_tree);
        cout << "OK\n";
    }

    void remove(char *key) {
        node_ptr left_tree_0 = nullptr;
        node_ptr right_tree_0 = nullptr;
        node_ptr left_tree = nullptr;
        node_ptr right_tree = nullptr;
        split(root, key, left_tree_0, right_tree_0);
        size_t len = strlen(key);
        key[strlen(key)] = 1;
        key[strlen(key) + 1] = '\0';
        split(right_tree_0, key, left_tree, right_tree);
        if (left_tree != nullptr) {
            cout << "OK\n";
            root = merge(left_tree_0, right_tree);
            delete left_tree;
            return;
        }
        cout << "NoSuchWord\n";
        right_tree_0 = merge(left_tree, right_tree);
        root = merge(left_tree_0, right_tree_0);
    }
};

void convertToLowercase(char *str) {
    for (size_t i = 0; str[i] != '\0'; ++i) {
        if ('A' <= str[i] && str[i] <= 'Z') {
            str[i] = str[i] - 'A' + 'a';
        }
    }
}

int main() {
    bst tree;
    int command;
    char input[MAX_KEY_LEN] = {0};
    uint64_t value;
    while (cin >> input) {
        convertToLowercase(input);
        if (input[0] == '+') {
            cin >> input >> value;
            convertToLowercase(input);
            tree.insert(input, value);
        } else if (input[0] == '-') {
            cin >> input;
            convertToLowercase(input);
            tree.remove(input);
        } else {
            tree.find(input);
        }
    }
    return 0;
}