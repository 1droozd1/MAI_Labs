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
        uint64_t value;              // Value associated with the key
    
        int y;                       // Random value used for balancing
    
        // Constructor
        node(const char *_key, uint64_t _value) {
            left = nullptr;
            right = nullptr;
    
            key = new char[MAX_KEY_LEN];  // Allocate memory for key string
            memcpy(key, _key, MAX_KEY_LEN);
    
            value = _value;
    
            y = rand();               // Generate a random value for balancing
        }
    
        // Destructor
        ~node() {
            delete[] key;             // Deallocate memory for key string
        }
    };
    
    using node_point = node *;

    node_point root;

    bst() {
        root = nullptr;
    }
    // Destructor of tree
    void destroy(node_point tree) {
        if (tree == nullptr) return;
        destroy(tree->left);
        destroy(tree->right);
        delete tree;
    }
    ~bst() {
        destroy(root);
    }
    // Merge two trees
    node_point merge(node_point L, node_point R) {
        if (L == nullptr) {
            return R;
        }
        if (R == nullptr) {
            return L;
        }

        if (L->y > R->y) {
            L->right = merge(L->right, R);
            return L;
        } else {
            R->left = merge(L, R->left);
            return R;
        }
    }
    // Splits two trees based on key
    void split(node_point tree, const char *key, node_point& L, node_point& R) {
        if (tree == nullptr) {
            L = nullptr;
            R = nullptr;
            return;
        }
        if (strcmp(tree->key, key) < 0) {
            split(tree->right, key, tree->right, R);
            L = tree;
        } else {
            split(tree->left, key, L, tree->left);
            R = tree;
        }
    }

    // Cheaking if min elem in tree
    node_point min_node(node_point pointer) {
        if (pointer == nullptr) return nullptr;
        if (pointer->left == nullptr) return pointer;
        return min_node(pointer->left);
    }

    // Function to search key
    node_point search(node_point tree, const char *key) {
        if (tree == nullptr) return nullptr;

        int search_mean = strcmp(tree->key, key); // value to define the search

        if (search_mean < 0) {
            return search(tree->right, key);
        } else if (search_mean > 0) {
            return search(tree->left, key);
        } else {
            return tree;
        }
    }

    // Find key in the tree
    void find(const char *key) {
        node_point elem = search(root, key);
        if (elem != nullptr) {
            cout << "OK: " << elem->value << "\n";
            return;
        }
        cout << "NoSuchWord\n";
    }

    // Insert new key in the tree
    void insert(const char *key, uint64_t value) {
        node_point left_tree = nullptr;
        node_point right_tree = nullptr;
        node_point elem = nullptr;

        split(root, key, left_tree, right_tree);

        elem = min_node(right_tree);

        // Cheaking of existence element in node
        if (elem != nullptr && strcmp(elem->key, key) == 0) {
            cout << "Exist\n";
            root = merge(left_tree, right_tree);
            return;
        }

        node_point new_node = new node(key, value);

        root = merge(merge(left_tree, new_node), right_tree);
        cout << "OK\n";
    }

    void remove(char *key) {

        node_point left_tree_0 = nullptr;
        node_point right_tree_0 = nullptr;
        node_point left_tree = nullptr;
        node_point right_tree = nullptr;

        // Spliting default tree into two subtrees based on the given key
        split(root, key, left_tree_0, right_tree_0);

        size_t len = strlen(key);
        key[strlen(key)] = 1;
        key[strlen(key) + 1] = '\0';

        split(right_tree_0, key, left_tree, right_tree);

        // Delete key from tree
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

// Converter to lowercase
void converter_to_lower(char *string) {
    for (size_t i = 0; string[i] != '\0'; ++i) {
        if ('A' <= string[i] && string[i] <= 'Z') {
            string[i] = string[i] - 'A' + 'a';
        }
    }
}

int main() {
    
    bst tree;
    int command;
    char input[MAX_KEY_LEN] = {0};
    uint64_t value;

    while (cin >> input) {

        converter_to_lower(input);

        switch (input[0])
        {
        case '+':
            cin >> input >> value;
            converter_to_lower(input);
            tree.insert(input, value);
            break;
        case '-':
            cin >> input;
            converter_to_lower(input);
            tree.remove(input);
            break;
        default:
            tree.find(input);
            break;
        }
    }
    return 0;
}