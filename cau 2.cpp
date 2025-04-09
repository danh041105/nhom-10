#include <bits/stdc++.h>
#define ll long long
#define faster ios::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
using namespace std;

int uutien(char dau){
    if(dau == '^') return 3;
    if(dau == '*' || dau == '/') return 2; 
    if(dau == '+' || dau == '-') return 1; 
    return 0;  // Trường hợp khác (như dấu ngoặc)
}

int main(){
    faster;
    string bieuthuc;
    getline(cin, bieuthuc);
    stack<char> st;
    string kqua = "";
    for(int i = 0; i < bieuthuc.size(); i++){
        if(bieuthuc[i] == ' ') continue;
        else if(isdigit(bieuthuc[i])){
            // xử lí trường hợp số có nhiều chữ số
            while(i < bieuthuc.size() && isdigit(bieuthuc[i])){
                kqua += bieuthuc[i];
                i++;
            }
            kqua += ' ';
            i--;  // Lùi lại vì vòng for sẽ tăng i
        }
        else if(bieuthuc[i] == '('){
            st.push(bieuthuc[i]);
        }
        else if(bieuthuc[i] == ')'){
            while(!st.empty() && st.top() != '('){
                kqua += st.top();
                kqua += ' ';
                st.pop();
            }
            if(!st.empty()) st.pop();
        }
        else{
            // đẩy các toán tử có độ ưu tiên >= toán tử hiện tại
            while(!st.empty() && uutien(st.top()) >= uutien(bieuthuc[i])){
                kqua += st.top();
                kqua += ' ';
                st.pop();
            }
            st.push(bieuthuc[i]);  // đẩy toán tử hiện tại vào stack
        }
    }
    // xử lí nốt các dấu còn lại trong stack
    while(!st.empty() && st.top() != '('){
        kqua += st.top();
        kqua += ' ';
        st.pop();
    }
    cout << kqua;
    return 0;
}