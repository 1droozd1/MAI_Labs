#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

class ModifiedTrie {
private:
    struct TrieNode {
        int left;
        int right;
        int index;
        map<char, int> children;

        TrieNode() : left(-1), right(-1), index(-1) {}
    };

    vector<TrieNode> nodes;
    string inputText;

    void AddNode(int left, int right) {
        int current = 0;
        int oldLeft = left;

        while (left <= right) {
            if (current == 0) {
                if (nodes[current].children.find(inputText[left]) != nodes[current].children.end()) {
                    current = nodes[current].children[inputText[left]];
                }

                if (current == 0) {
                    CreateTrieNode(left, right, oldLeft);
                    nodes[current].children[inputText[left]] = nodes.size() - 1;
                    break;
                }
            }

            int start = nodes[current].left;
            int finish = nodes[current].right;
            bool split = false;

            for (int i = start; (i <= finish) && (left + i - start <= right); ++i) {
                if (inputText[i] != inputText[left + i - start]) {
                    nodes[current].right = i - 1;
                    int oldIndex = nodes[current].index;
                    nodes[current].index = -1;

                    if (inputText[finish] == '$')
                        CreateTrieNode(i, finish, oldIndex);
                    else
                        CreateTrieNode(i, finish);

                    nodes[nodes.size() - 1].children = nodes[current].children;
                    nodes[current].children.clear();
                    nodes[current].children[inputText[i]] = nodes.size() - 1;

                    CreateTrieNode(left + i - start, right, oldLeft);
                    nodes[current].children[inputText[left + i - start]] = nodes.size() - 1;

                    split = true;
                    break;
                }
            }

            if (!split) {
                int newLeft = left + finish - start + 1;
                if (nodes[current].children.find(inputText[newLeft]) != nodes[current].children.end()) {
                    current = nodes[current].children[inputText[newLeft]];
                } else {
                    CreateTrieNode(newLeft, right, oldLeft);
                    nodes[current].children[inputText[newLeft]] = nodes.size() - 1;
                    break;
                }
                left = newLeft;
            } else {
                break;
            }
        }
    }

    void CreateTrieNode(int left, int right) {
        nodes.emplace_back(TrieNode());
        nodes.back().left = left;
        nodes.back().right = right;
    }

    void CreateTrieNode(int left, int right, int index) {
        nodes.emplace_back(TrieNode());
        nodes.back().left = left;
        nodes.back().right = right;
        nodes.back().index = index;
    }

    vector<int> FindOccurrences(const string& pattern) {
        vector<int> result;
        int current = 0;
        int left = 0;
        int right = pattern.length() - 1;
        bool flag = false;

        while (left <= right) {
            if (current == 0) {
                if (nodes[current].children.find(pattern[left]) != nodes[current].children.end())
                    current = nodes[current].children[pattern[left]];
                else
                    break;
            }

            int start = nodes[current].left;
            int finish = nodes[current].right;

            for (int i = 0; (start + i <= finish) && (i + left <= right); ++i) {
                if (pattern[i + left] != inputText[start + i]) {
                    flag = true;
                    break;
                }
            }

            if (!flag) {
                left = left + finish - start + 1;

                if (left > right)
                    break;

                if (nodes[current].children.find(pattern[left]) != nodes[current].children.end())
                    current = nodes[current].children[pattern[left]];
                else
                    break;
            } else {
                break;
            }
        }

        if ((left > right) && (!flag) && (!pattern.empty()))
            DFS(result, current);

        return result;
    }

    void DFS(vector<int>& result, int current) {
        if (nodes[current].children.empty())
            result.push_back(nodes[current].index);

        for (const auto& [first, second] : nodes[current].children)
            DFS(result, second);
    }

public:
    void ExecuteAlgorithm() {
        getline(cin, inputText);
        inputText += '$';
        nodes.emplace_back(TrieNode());

        for (size_t i = 0; i < inputText.length(); ++i)
            AddNode(i, inputText.length() - 1);

        string pattern;
        int counter = 1;

        while (getline(cin, pattern)) {
            vector<int> result = FindOccurrences(pattern);

            if (!result.empty()) {
                cout << counter << ": ";
                sort(result.begin(), result.end());

                for (size_t i = 0; i < result.size(); ++i) {
                    if (i != 0)
                        cout << ", ";
                    cout << result[i] + 1;
                }

                cout << "\n";
            }

            ++counter;
        }
    }
};

int main() {
    ModifiedTrie algo;
    algo.ExecuteAlgorithm();
    return 0;
}
