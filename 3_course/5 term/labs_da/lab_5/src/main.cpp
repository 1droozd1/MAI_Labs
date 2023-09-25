#include <iostream>
#include <map>
#include <set>
#include <string>

class SuffixTreeNode {
public:
    int start;
    int *end;
    std::map<char, SuffixTreeNode*> edges;
    int suffixNumber;
    SuffixTreeNode *suffixLink;

    SuffixTreeNode(int start, int *end, int suffixNumber, SuffixTreeNode *suffixLink = nullptr) 
        : start(start), end(end), suffixNumber(suffixNumber), suffixLink(suffixLink) {}
    
    int Length() {
        return *end - start + 1;
    }

    ~SuffixTreeNode() {
        for (auto edge : edges) {
            delete edge.second;
        }
    }
};

class SuffixTree {
private:
    SuffixTreeNode *root;
    SuffixTreeNode *lastCreatedNode;
    SuffixTreeNode *currentNode;
    int currentLength;
    int currentEdge;
    int cnt;
    int globalEnd;
    std::string text;

    void Insert(int iter);
    void DFS(SuffixTreeNode *node, std::set<int> &output);
    
public:
    SuffixTree(const std::string &text);
    ~SuffixTree();
    void Find(const std::string &pattern, std::set<int> &output);
};

SuffixTree::SuffixTree(const std::string &inputText) : text(inputText + "$"), 
    currentLength(0), currentEdge(-1), cnt(0), globalEnd(-1) {
    root = new SuffixTreeNode(-1, new int(-1), -1);
    currentNode = root;
    for (int i = 0; i < text.size(); i++) {
        Insert(i);
    }
}

SuffixTree::~SuffixTree() {
    delete root;
}

void SuffixTree::Insert(int iter) {
    lastCreatedNode = nullptr;
    globalEnd++;
    cnt++;

    while (cnt > 0) {
        if (currentLength == 0) {
            currentEdge = iter;
        }
        if (currentNode->edges.find(text[currentEdge]) == currentNode->edges.end()) {
            currentNode->edges[text[iter]] = new SuffixTreeNode(iter, &globalEnd, iter - cnt + 1, root);
            if (lastCreatedNode != nullptr) {
                lastCreatedNode->suffixLink = currentNode;
                lastCreatedNode = nullptr;
            }
        } else {
            SuffixTreeNode *childNode = currentNode->edges[text[currentEdge]];
            
            if (currentLength >= childNode->Length()) {
                currentEdge += childNode->Length();
                currentLength -= childNode->Length();
                currentNode = childNode;
                continue;
            }

            if (text[childNode->start + currentLength] == text[iter]) {
                if (lastCreatedNode != nullptr && currentNode != root) {
                    lastCreatedNode->suffixLink = currentNode;
                }
                currentLength++;
                break;
            }

            int *splitPoint = NULL;
            splitPoint = new int;
            *splitPoint = (childNode->start + currentLength - 1);
            SuffixTreeNode *splitNode = new SuffixTreeNode(childNode->start, splitPoint, -1, root);
            currentNode->edges[text[currentEdge]] = splitNode;
            splitNode->edges[text[iter]] = new SuffixTreeNode(iter, &globalEnd, iter - cnt + 1, root);
            childNode->start += currentLength;
            splitNode->edges[text[childNode->start]] = childNode;

            if (lastCreatedNode != nullptr) {
                lastCreatedNode->suffixLink = splitNode;
            }
            lastCreatedNode = splitNode;
        }
        
        cnt--;

        if (currentNode == root && currentLength > 0) {
            currentLength--;
            currentEdge++;
        } else if (currentNode != root) {
            currentNode = currentNode->suffixLink;
        }
    }
}

void SuffixTree::Find(const std::string &pattern, std::set<int> &output) {
    if (pattern.empty()) {
        return;
    }

    SuffixTreeNode *current = root;
    int length = 0;

    while (length < pattern.length()) {
        if (current->edges.find(pattern[length]) == current->edges.end()) {
            return;
        }

        SuffixTreeNode *child = current->edges[pattern[length]];

        for (int i = 0; i < child->Length(); i++) {
            if (length + i >= pattern.length()) {
                DFS(child, output);
            }

            if (pattern[length + i] != text[child->start + i]) {
                return;
            }
        }

        current = child;
        length += child->Length();
    }
    DFS(current, output);
}

void SuffixTree::DFS(SuffixTreeNode *node, std::set<int> &output) {
    if (node->suffixNumber > -1) {
        output.insert(node->suffixNumber);
    }
    for (auto edge : node->edges) {
        DFS(edge.second, output);
    }
}


int main() {
    std::string text;
    std::cin >> text;
    SuffixTree tree(text);
    
    std::string pattern;
    int idx = 1;
    std::cin.ignore();
    while (std::getline(std::cin, pattern)) {
        if (pattern.empty()) continue;

        std::set<int> positions;
        tree.Find(pattern, positions);
        
        if (!positions.empty()) {
            std::cout << idx << ":";
            int i = 0;
            for (const int pos : positions) {
                std::cout << pos + 1;
                if (i++ != positions.size() - 1) {
                    std::cout << ",";
                }
            }
            std::cout << std::endl;
        }
        idx++;
    }

    return 0;
}