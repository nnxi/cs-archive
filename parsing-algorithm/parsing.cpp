#include <iostream>
#include <string>
using namespace std;

class Passing {  // 값 전달용
public:
    double front;
    double end;
    int front_index;
    int end_index;
};

string firstcalc(string s);
double secondcalc(double front, double end, char c);
Passing div(string s, int index);

int main() {
    string s, temp;
    double result;

    while (1) {
        cout << "아래에 계산식을 입력하세요(x 입력 시 종료)" << "\n";
        getline(cin, s);

        if (s == "x")
            break;

        while (s.find(' ') != -1)  // 공백 삭제
            s.erase(s.find(' '), 1);

        temp = firstcalc(s);
        if (temp[0] == '-') {  // 음수라면 부호 지우고 먼저 실수로 변형 후 -1 곱함
            temp.erase(0, 1);
            result = stod(temp) * -1;
        }
        else
            result = stod(temp);

        cout << "답 : " << result << "\n\n";
    }
}

string firstcalc(string s) {
    string temp;
    int st, en, middle;
    double t;
    Passing p;

    while (s.find('(') != -1) {  // 괄호가 있다면 먼저 처리
        st = s.find('(');
        en = s.find(')', st);
        temp = firstcalc(s.substr(st + 1, en - st - 1));  // 괄호를 제외하고 재귀호출
        s.erase(st, en - st + 1);  // 괄호 포함 삭제
        s.insert(st, temp);  // 계산된 값으로 대체
    }

    while (s.find('*') != -1 || s.find('/') != -1) {  // 연산의 우선순위 고려
        if (s.find('*') != -1) {
            middle = s.find('*');
            p = div(s, middle);
            t = secondcalc(p.front, p.end, '*');
        }
        else {
            middle = s.find('/');
            p = div(s, middle);
            t = secondcalc(p.front, p.end, '/');
        }

        s.erase(p.front_index, p.end_index - p.front_index + 1);  // 계산된 값으로 대체
        s.insert(p.front_index, to_string(t));
    }

    while (s.find('+') != -1 || (s.find('-') != -1 && s.rfind('-') != 0)) {
        if (s.find("--") != -1) {
            middle = s.find("--");
            s.erase(middle, 2);
            s.insert(middle, "+");
        }

        if (s.find('+') != -1) {
            middle = s.find('+');
            p = div(s, middle);
            t = secondcalc(p.front, p.end, '+');
        }
        else if (s.find('-') != -1) {
            middle = s.find('-');
            p = div(s, middle);
            t = secondcalc(p.front, p.end, '-');
        }

        s.erase(p.front_index, p.end_index - p.front_index + 1);  // 계산된 값으로 대체
        s.insert(p.front_index, to_string(t));
    }

    return s;
}

double secondcalc(double front, double end, char c) {  // 실질적 계산
    switch (c) {
    case '*':
        return front * end;
    case '/':
        return front / end;
    case '+':
        return front + end;
    case '-':
        return front - end;
    default:
        return 0;
    }
}

Passing div(string s, int index) {  // 주어진 연산자 위치를 중심으로 양쪽으로 인덱스 전개
    Passing p;
    int st = index - 1;
    int en = index + 1;
    bool is_fminus = false;
    bool is_eminus = false;

    if (s[en] == '-') {  // 오른쪽 값 부호 판별
        is_eminus = true;
        en++;
    }

    while (st >= 0 && (isdigit(s[st]) || s[st] == '.')) {  // 왼쪽 값이 숫자거나 .이면 인덱스 전개
        st--;
    }

    if (st >= 0 && s[st] == '-') {  // 왼쪽 값 부호 판별
        if (st == 0)
            is_fminus = true;
        else if (!isdigit(s[st - 1]))
            is_fminus = true;
        st++;
    }
    else {
        st++;
    }

    while (en < s.length() && (isdigit(s[en]) || s[en] == '.')) {  // 오른쪽 값 인덱스 이동
        en++;
    }
    en--;

    p.front = stod(s.substr(st, index - st));  // 왼쪽 값 추출
    p.front_index = st;

    if (is_fminus) {  // 부호에 맞게 값 변경
        p.front *= -1;
        p.front_index--;
    }

    p.end_index = en;
    if (is_eminus) {
        p.end = stod(s.substr(index + 2, en - index - 1));
    }
    else {
        p.end = stod(s.substr(index + 1, en - index));
    }

    if (is_eminus) {  // 부호에 맞게 값 변경
        p.end *= -1;
    }

    return p;
}
