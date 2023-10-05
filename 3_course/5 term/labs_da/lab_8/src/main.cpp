#include <iostream>
#include <vector>
#include <math.h>

using namespace std;

int main() {
    long long nomin, money; // nomin - степени, money - номинал денег
    cin >> nomin >> money;
    long long amount; // amount - количество денег, которые надо разменять
    cin >> amount;

    vector<long long> kol_money(nomin, 0);

    while (amount != 0) {
        if (amount - pow(money, nomin - 1) >= 0) {
            amount -= pow(money, nomin - 1);
            kol_money[nomin - 1] += 1;
        } else {
            nomin -= 1;
        }
    }

    for (int i = 0; i <= kol_money.size() - 1; i++) {
        cout << kol_money[i] << "\n";
    }

    return 0;
}