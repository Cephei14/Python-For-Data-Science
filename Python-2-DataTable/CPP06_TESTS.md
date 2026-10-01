# C++ Module 06 – Test Plan

Tests for **ex00 (ScalarConverter)**, **ex01 (Serializer)** and **ex02 (Identify real type)**, plus checks for the general rules of the subject.

Assumptions (adapt the names if yours differ):

```
cpp06/
├── ex00/  Makefile  ScalarConverter.{hpp,cpp}  main.cpp        -> binary: convert
├── ex01/  Makefile  Serializer.{hpp,cpp}  Data.{hpp,cpp}  main.cpp
└── ex02/  Makefile  Base.{hpp,cpp}  A.{hpp,cpp}  B.{hpp,cpp}  C.{hpp,cpp}  main.cpp
```

Common compile line used below:

```bash
FLAGS="-Wall -Wextra -Werror -std=c++98"
```

---

## 0. General rules checks (run from `cpp06/`)

### 0.1 Build and Makefile

```bash
for d in ex00 ex01 ex02; do
  echo "=== $d ==="
  (cd $d && make re >/dev/null && echo "build OK")
  (cd $d && make 2>&1 | grep -qiE "nothing to be done|up to date" && echo "no relink OK" || echo "!! relinks (Makefile bug)")
  (cd $d && make -n re | grep -E "c\+\+|g\+\+|clang" | head -1 | grep -q -- "-Wall -Wextra -Werror" && echo "flags OK" || echo "!! flags missing")
  (cd $d && make fclean >/dev/null && echo "fclean OK")
done
```

Expected: every exercise prints `build OK`, `no relink OK`, `flags OK`, `fclean OK`.
Also check by hand that the Makefile has the rules `$(NAME)`, `all`, `clean`, `fclean`, `re` and uses `c++`.

### 0.2 Forbidden stuff (should print nothing)

```bash
# using namespace / friend  (-42)
grep -rnE "using +namespace|\bfriend\b" --include=*.cpp --include=*.hpp --include=*.h .

# forbidden C functions (0)
grep -rnE "\b(printf|fprintf|sprintf|snprintf|malloc|calloc|realloc|free)\s*\(" --include=*.cpp --include=*.hpp --include=*.h .

# STL containers / algorithms before module 08 (-42)
grep -rnE "#include *<(vector|list|map|set|stack|queue|deque|algorithm|iterator)>" --include=*.cpp --include=*.hpp --include=*.h .

# ex02: typeinfo is forbidden
grep -rnE "typeinfo|typeid" ex02/

# C++11 stuff
grep -rnE "\b(nullptr|auto|override|constexpr|std::to_string|std::stoi|std::stod|std::stof)\b" --include=*.cpp --include=*.hpp .
```

### 0.3 Headers

```bash
# headers WITHOUT include guards (should print nothing)
grep -rLE "#ifndef|#pragma once" --include=*.hpp --include=*.h .

# each header compiles on its own (self-contained)
for h in $(find . -name "*.hpp" -o -name "*.h"); do
  echo "#include \"$h\"" > /tmp/hdr_test.cpp
  c++ $FLAGS -fsyntax-only -I$(dirname $h) /tmp/hdr_test.cpp 2>/dev/null && echo "OK   $h" || echo "FAIL $h"
done

# including twice must work (double inclusion)
for h in $(find . -name "*.hpp" -o -name "*.h"); do
  printf '#include "%s"\n#include "%s"\n' "$h" "$h" > /tmp/hdr_test2.cpp
  c++ $FLAGS -fsyntax-only -I$(dirname $h) /tmp/hdr_test2.cpp 2>/dev/null && echo "OK   $h" || echo "FAIL $h"
done
```

### 0.4 Right cast in the right exercise (module's additional rule)

```bash
echo "--- C-style casts (should be empty, review manually) ---"
grep -rnE "\((unsigned +)?(int|char|float|double|long|short|uintptr_t|Data|Base|A|B|C)\s*\*?\s*\)\s*[A-Za-z_&*(0-9]" --include=*.cpp --include=*.hpp .

echo "--- ex00 ---"; grep -rn "static_cast"      ex00/ | head
echo "--- ex01 ---"; grep -rn "reinterpret_cast" ex01/ | head
echo "--- ex02 ---"; grep -rn "dynamic_cast"     ex02/ | head
```

Expected:
- ex00 -> `static_cast` (scalar to scalar conversions)
- ex01 -> `reinterpret_cast` (pointer <-> integer)
- ex02 -> `dynamic_cast` (pointer version AND reference version)

### 0.5 Leaks / UB (run for each final binary)

```bash
valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=42 ./your_binary [args]
# or without valgrind:
c++ -g -fsanitize=address,undefined -std=c++98 *.cpp -o san && ./san [args]
```

Expected: `All heap blocks were freed` and no errors.

---

## 1. ex00 – ScalarConverter

### 1.1 Automated table of tests

Save as `ex00/run_tests.sh`, then `make && bash run_tests.sh`.

`*` in an expected line means "do not compare this line" (used where the subject leaves room for interpretation).

```bash
#!/bin/bash
BIN=./convert
pass=0; fail=0

check() {
  local input="$1"; shift
  local -a exp=("$@")
  local got lines ok=1
  got=$($BIN "$input" 2>&1)
  mapfile -t lines <<< "$got"
  [ "${#lines[@]}" -ne 4 ] && ok=0
  for i in 0 1 2 3; do
    [ "${exp[$i]}" = "*" ] && continue
    [ "${exp[$i]}" = "${lines[$i]}" ] || ok=0
  done
  if [ $ok -eq 1 ]; then
    pass=$((pass+1)); echo "[ OK ] ./convert \"$input\""
  else
    fail=$((fail+1)); echo "[FAIL] ./convert \"$input\""
    echo "   expected:"; printf '     %s\n' "${exp[@]}"
    echo "   got:";      printf '     %s\n' "${lines[@]}"
  fi
}

# robustness: must not crash / hang (exit code < 128, finishes in 2s)
nocrash() {
  local out rc
  out=$(timeout 2 $BIN "$@" 2>&1); rc=$?
  if [ $rc -ge 124 ]; then echo "[FAIL] crash/hang (rc=$rc) with args: $*"; fail=$((fail+1))
  else echo "[ OK ] no crash: [$*] -> $(echo "$out" | tr '\n' '|')"; pass=$((pass+1)); fi
}

echo "##### Examples from the subject"
check "0"     "char: Non displayable" "int: 0"  "float: 0.0f"  "double: 0.0"
check "nan"   "char: impossible" "int: impossible" "float: nanf" "double: nan"
check "42.0f" "char: '*'" "int: 42" "float: 42.0f" "double: 42.0"

echo "##### char literals"
check "a"     "char: 'a'" "int: 97" "float: 97.0f" "double: 97.0"
check "'a'"   "char: 'a'" "int: 97" "float: 97.0f" "double: 97.0"
check "Z"     "char: 'Z'" "int: 90" "float: 90.0f" "double: 90.0"
check "*"     "char: '*'" "int: 42" "float: 42.0f" "double: 42.0"
check "~"     "char: '~'" "int: 126" "float: 126.0f" "double: 126.0"
check "5"     "char: Non displayable" "int: 5" "float: 5.0f" "double: 5.0"   # a digit is an INT, not the char '5'

echo "##### int literals / char boundaries"
check "42"    "char: '*'" "int: 42" "float: 42.0f" "double: 42.0"
check "-42"   "*"         "int: -42" "float: -42.0f" "double: -42.0"
check "31"    "char: Non displayable" "int: 31"  "float: 31.0f"  "double: 31.0"
check "32"    "char: ' '" "int: 32"  "float: 32.0f"  "double: 32.0"
check "126"   "char: '~'" "int: 126" "float: 126.0f" "double: 126.0"
check "127"   "char: Non displayable" "int: 127" "float: 127.0f" "double: 127.0"
check "128"   "*"         "int: 128" "float: 128.0f" "double: 128.0"
check "255"   "*"         "int: 255" "float: 255.0f" "double: 255.0"

echo "##### int limits"
check "2147483647"   "char: impossible" "int: 2147483647"  "float: 2147483648.0f" "double: 2147483647.0"
check "-2147483648"  "*"                "int: -2147483648" "float: -2147483648.0f" "double: -2147483648.0"
check "2147483648"   "char: impossible" "int: impossible"  "float: 2147483648.0f" "double: 2147483648.0"
check "-2147483649"  "*"                "int: impossible"  "float: -2147483648.0f" "double: -2147483649.0"
check "99999999999"  "char: impossible" "int: impossible"  "float: 99999997952.0f" "double: 99999999999.0"

echo "##### float literals"
check "0.0f"  "char: Non displayable" "int: 0" "float: 0.0f" "double: 0.0"
check "4.2f"  "char: Non displayable" "int: 4" "float: 4.2f" "double: 4.2"
check "-4.2f" "*"                     "int: -4" "float: -4.2f" "double: -4.2"
check "42.5f" "char: '*'" "int: 42" "float: 42.5f" "double: 42.5"
check "65.0f" "char: 'A'" "int: 65" "float: 65.0f" "double: 65.0"

echo "##### double literals"
check "0.0"   "char: Non displayable" "int: 0" "float: 0.0f" "double: 0.0"
check "4.2"   "char: Non displayable" "int: 4" "float: 4.2f" "double: 4.2"
check "-4.2"  "*"                     "int: -4" "float: -4.2f" "double: -4.2"
check "42.0"  "char: '*'" "int: 42" "float: 42.0f" "double: 42.0"
check "1000000.5" "char: impossible" "int: 1000000" "float: 1000000.5f" "double: 1000000.5"
check "2147483648.0" "char: impossible" "int: impossible" "float: 2147483648.0f" "double: 2147483648.0"
# bigger than FLOAT_MAX: float must be impossible (or inf), double is fine
check "1000000000000000000000000000000000000000.0" "char: impossible" "int: impossible" "*" "*"

echo "##### pseudo literals"
check "nanf"  "char: impossible" "int: impossible" "float: nanf"  "double: nan"
check "nan"   "char: impossible" "int: impossible" "float: nanf"  "double: nan"
check "-inff" "char: impossible" "int: impossible" "float: -inff" "double: -inf"
check "+inff" "char: impossible" "int: impossible" "float: +inff" "double: +inf"
check "-inf"  "char: impossible" "int: impossible" "float: -inff" "double: -inf"
check "+inf"  "char: impossible" "int: impossible" "float: +inff" "double: +inf"

echo "##### garbage input (must not crash; output format up to you,"
echo "#####                   recommended: all 4 lines 'impossible')"
for s in "abc" "" " " "42ff" "4.2.2" "++1" "--5" "+-3" "." ".f" "f" "4.2ff" "nanff" "NAN" "Inf" "0x1A" "1e5" "42abc" "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"; do
  nocrash "$s"
done
nocrash                 # no argument
nocrash 1 2 3           # too many arguments

echo
echo "RESULT: $pass passed, $fail failed"
[ $fail -eq 0 ]
```

### 1.2 Manual checks on output format

```bash
./convert 42.0f | cat -A     # every line must end with '$' (newline), nothing else
./convert 0 > /dev/null 2>&1; echo $?   # normal run => exit 0
./convert 42 2>/dev/null     # results must be on STDOUT (not stderr)
```

Checklist:
- [ ] `float` always ends with `f`, `double` never does (`42.0f` / `42.0`)
- [ ] There is always at least one digit after the dot (`0.0f`, not `0f` / `0.00000`)
- [ ] `char` shows the character between single quotes: `'*'`
- [ ] Non printable chars (0-31 and 127) -> `Non displayable`; out of range / NaN / inf -> `impossible`
- [ ] Overflowing int -> `int: impossible` (no wrap-around garbage like `-2147483648`)
- [ ] The type detection is done **before** converting (int vs float vs double vs char vs pseudo-literals)

### 1.3 The class must NOT be instantiable

Each snippet below **must fail to compile**:

```bash
cd ex00
snippets=(
  'ScalarConverter a;'
  'ScalarConverter *p = new ScalarConverter();'
  'const ScalarConverter &r = *(ScalarConverter*)0; ScalarConverter b(r);'
  'ScalarConverter &r = *(ScalarConverter*)0; ScalarConverter &s = *(ScalarConverter*)0; r = s;'
)
for s in "${snippets[@]}"; do
  printf '#include "ScalarConverter.hpp"\nint main(){ %s }\n' "$s" > /tmp/inst.cpp
  if c++ $FLAGS -I. -fsyntax-only /tmp/inst.cpp 2>/dev/null; then
    echo "[FAIL] compiles (should not): $s"
  else
    echo "[ OK ] rejected: $s"
  fi
done

# and this one MUST compile:
printf '#include "ScalarConverter.hpp"\nint main(){ ScalarConverter::convert("42"); }\n' > /tmp/ok.cpp
c++ $FLAGS -I. -fsyntax-only /tmp/ok.cpp && echo "[ OK ] static convert() usable"
```

Also check by reading the header: only **one** public method (`static void convert(const std::string&)`), constructors / copy-ctor / operator= / destructor are private (Orthodox Canonical Form, but not instantiable).

---

## 2. ex01 – Serializer

### 2.1 Test program

Save as `ex01/test_serializer.cpp`. Adapt the `Data` construction to your own struct (it must have at least one data member).

```cpp
#include <iostream>
#include <stdint.h>      // uintptr_t in C++98 (<cstdint> is C++11)
#include "Serializer.hpp"
#include "Data.hpp"

static int g_fail = 0;
#define CHECK(cond, msg) do { \
    if (cond) std::cout << "[ OK ] " << msg << std::endl; \
    else { std::cout << "[FAIL] " << msg << std::endl; g_fail++; } } while (0)

int main()
{
    // --- Data must be non-empty (an empty struct has sizeof == 1)
    CHECK(sizeof(Data) > 1, "Data is not empty (sizeof = " << sizeof(Data) << ")");

    // --- 1. object on the stack
    Data stackData;                       // <- fill members if needed
    uintptr_t raw = Serializer::serialize(&stackData);
    Data *back = Serializer::deserialize(raw);
    CHECK(back == &stackData, "stack: deserialize(serialize(p)) == p");
    CHECK(raw == reinterpret_cast<uintptr_t>(&stackData), "stack: raw value is the real address");

    // --- 2. object on the heap
    Data *heapData = new Data();
    uintptr_t raw2 = Serializer::serialize(heapData);
    CHECK(Serializer::deserialize(raw2) == heapData, "heap: round trip gives same pointer");
    CHECK(raw2 != raw, "two different objects => two different raw values");

    // --- 3. members are still reachable / unchanged through the new pointer
    //     (adapt: set a member, serialize, deserialize, read the member back)
    //     heapData->someMember = 42;
    //     CHECK(Serializer::deserialize(Serializer::serialize(heapData))->someMember == 42, "member preserved");

    // --- 4. NULL pointer
    CHECK(Serializer::serialize(NULL) == 0, "serialize(NULL) == 0");
    CHECK(Serializer::deserialize(0) == NULL, "deserialize(0) == NULL");

    // --- 5. double round trip
    CHECK(Serializer::deserialize(Serializer::serialize(
          Serializer::deserialize(Serializer::serialize(heapData)))) == heapData,
          "double round trip");

    delete heapData;
    std::cout << (g_fail ? "SOME TESTS FAILED" : "ALL TESTS PASSED") << std::endl;
    return g_fail != 0;
}
```

```bash
cd ex01
c++ $FLAGS -I. test_serializer.cpp Serializer.cpp Data.cpp -o test_ser   # drop Data.cpp if you have none
./test_ser
valgrind --leak-check=full ./test_ser 2>&1 | grep -E "ERROR SUMMARY|All heap"
```

> Your **own** `main.cpp` should also print the original pointer, the raw integer and the deserialized pointer so the evaluator can see they match.

### 2.2 Must NOT be instantiable

```bash
cd ex01
for s in 'Serializer s;' 'Serializer *p = new Serializer();'; do
  printf '#include "Serializer.hpp"\nint main(){ %s }\n' "$s" > /tmp/inst.cpp
  c++ $FLAGS -I. -fsyntax-only /tmp/inst.cpp 2>/dev/null \
    && echo "[FAIL] compiles: $s" || echo "[ OK ] rejected: $s"
done
```

### 2.3 Checklist

- [ ] Signatures exactly `static uintptr_t serialize(Data* ptr);` and `static Data* deserialize(uintptr_t raw);`
- [ ] Only `reinterpret_cast` is used (no C-style cast, no `static_cast`, no `union`)
- [ ] `Data` is a separate struct/class with its own files, turned in with the exercise
- [ ] Round trip compared with `==` against the original pointer
- [ ] Private constructors / destructor / copy / assignment in `Serializer`

---

## 3. ex02 – Identify real type

### 3.1 Test program

Save as `ex02/test_identify.cpp`. It uses `dynamic_cast` **in the tester** to know the ground truth, and captures what your `identify()` prints.

> If your `generate()` / `identify()` live in `main.cpp`, move them to `utils.cpp` (or similar) first, otherwise there will be two `main` functions. Declarations are written below so no extra header is needed.

```cpp
#include <iostream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include "Base.hpp"
#include "A.hpp"
#include "B.hpp"
#include "C.hpp"

Base *generate(void);
void  identify(Base *p);
void  identify(Base &p);

static int g_fail = 0;
#define CHECK(cond, msg) do { \
    if (cond) std::cout << "[ OK ] " << msg << std::endl; \
    else { std::cout << "[FAIL] " << msg << std::endl; g_fail++; } } while (0)

static std::string trim(std::string s)
{
    while (!s.empty() && (s[s.size()-1] == '\n' || s[s.size()-1] == ' '))
        s.erase(s.size() - 1);
    return s;
}
static std::string capturePtr(Base *p)
{
    std::ostringstream os;
    std::streambuf *old = std::cout.rdbuf(os.rdbuf());
    identify(p);
    std::cout.rdbuf(old);
    return trim(os.str());
}
static std::string captureRef(Base &p)
{
    std::ostringstream os;
    std::streambuf *old = std::cout.rdbuf(os.rdbuf());
    identify(p);
    std::cout.rdbuf(old);
    return trim(os.str());
}
static std::string truth(Base *p)
{
    if (dynamic_cast<A*>(p)) return "A";
    if (dynamic_cast<B*>(p)) return "B";
    if (dynamic_cast<C*>(p)) return "C";
    return "?";
}

int main()
{
    // 1. Known objects, created directly
    {
        A a; B b; C c;
        CHECK(capturePtr(&a) == "A", "identify(Base*) on A");
        CHECK(capturePtr(&b) == "B", "identify(Base*) on B");
        CHECK(capturePtr(&c) == "C", "identify(Base*) on C");
        Base &ra = a, &rb = b, &rc = c;
        CHECK(captureRef(ra) == "A", "identify(Base&) on A");
        CHECK(captureRef(rb) == "B", "identify(Base&) on B");
        CHECK(captureRef(rc) == "C", "identify(Base&) on C");
    }

    // 2. generate(): all three types must show up, and pointer/ref versions must agree with the truth
    std::srand(std::time(NULL));
    int count[3] = {0, 0, 0};
    const int N = 500;
    bool allAgree = true;
    for (int i = 0; i < N; ++i)
    {
        Base *p = generate();
        if (!p) { allAgree = false; break; }
        std::string t = truth(p);
        if (t == "A") count[0]++; else if (t == "B") count[1]++; else if (t == "C") count[2]++;
        if (capturePtr(p) != t || captureRef(*p) != t) allAgree = false;
        delete p;                       // virtual destructor => no leak, no UB
    }
    CHECK(allAgree, "identify(ptr) and identify(ref) match the real type for " << N << " random objects");
    std::cout << "       distribution  A=" << count[0] << " B=" << count[1] << " C=" << count[2] << std::endl;
    CHECK(count[0] > 0 && count[1] > 0 && count[2] > 0, "generate() returns A, B and C");
    CHECK(count[0] > N/10 && count[1] > N/10 && count[2] > N/10, "distribution is reasonably balanced (> 10% each)");

    std::cout << (g_fail ? "SOME TESTS FAILED" : "ALL TESTS PASSED") << std::endl;
    return g_fail != 0;
}
```

```bash
cd ex02
c++ $FLAGS -I. test_identify.cpp Base.cpp A.cpp B.cpp C.cpp utils.cpp -o test_id   # adapt file list
./test_id
valgrind --leak-check=full ./test_id 2>&1 | grep -E "ERROR SUMMARY|All heap"
```

> Common bug caught by the distribution test: calling `srand(time(NULL))` **inside** `generate()`. In a fast loop it returns the same type every time. Seed once (in `main`) or use another source of randomness.

### 3.2 Static checks

```bash
cd ex02
# Base must have only a public virtual destructor
cat Base.hpp

# A, B, C must publicly inherit from Base and be empty
grep -nE "class +(A|B|C)" A.hpp B.hpp C.hpp          # expect ": public Base"

# No typeinfo anywhere
grep -rnE "typeinfo|typeid|#include *<typeinfo>" . && echo "!! FORBIDDEN" || echo "typeinfo OK"

# Both dynamic_cast flavours present
grep -n "dynamic_cast" *.cpp
```

Read `identify(Base& p)` by hand:
- [ ] it contains **no pointer** (no `Base*`, no `&p` stored in a pointer, no `dynamic_cast<A*>`)
- [ ] it uses `dynamic_cast<A&>(p)` and handles the failure (throws) with `try/catch`
- [ ] catch with `catch (std::exception&)` or `catch (...)`, **not** `std::bad_cast` (its declaration lives in `<typeinfo>`, which is forbidden to include)
- [ ] output is exactly `A`, `B` or `C`, followed by a newline

Read `identify(Base* p)`:
- [ ] `dynamic_cast<A*>(p)` etc., checks the result against `NULL`
- [ ] does not crash when `p == NULL` (nice to have: prints nothing or an error message)

### 3.3 Quick manual run

Run your own `main` several times: the sequence of letters should differ between runs.

```bash
for i in 1 2 3 4 5; do ./ex02_binary | head -3; sleep 1; done
```

---

## 4. Likely defense questions

| Topic | Be ready to explain |
|-------|---------------------|
| ex00 | Why `static_cast` and not `reinterpret_cast`/C-cast? How do you detect the type of the string? What happens with `INT_MAX + 1`? Why `nanf` / `-inff` need special handling? |
| ex00 | Why is the class not instantiable and how did you enforce it? Difference between "impossible" and "Non displayable". |
| ex01 | What does `reinterpret_cast` do (and not do)? Is it safe? Why is `uintptr_t` used instead of `unsigned long`? What would break if the object was destroyed before deserialize? |
| ex02 | Why must `Base` have a virtual destructor? Why does `dynamic_cast` need a polymorphic type? What does `dynamic_cast` return on failure for a pointer vs a reference? Why can't you reuse the pointer version inside the reference version? |
| General | `static_cast` vs `dynamic_cast` vs `reinterpret_cast` vs `const_cast`: one use case of each. |

---

## 5. Final one-shot sanity script (optional)

```bash
#!/bin/bash
FLAGS="-Wall -Wextra -Werror -std=c++98"
for d in ex00 ex01 ex02; do
  echo "######## $d"
  (cd $d && make re >/dev/null 2>&1 && echo "build OK" || echo "!! build failed")
done
(cd ex00 && bash run_tests.sh | tail -1)
(cd ex01 && c++ $FLAGS -I. test_serializer.cpp Serializer.cpp Data.cpp -o t 2>&1 | head -5 && ./t | tail -1; rm -f t)
(cd ex02 && c++ $FLAGS -I. test_identify.cpp Base.cpp A.cpp B.cpp C.cpp utils.cpp -o t 2>&1 | head -5 && ./t | tail -1; rm -f t)
```
