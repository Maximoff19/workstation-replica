# Skill: Algoritmia - Programación Competitiva

## Descripción

Skill especializada en algoritmos y estructuras de datos para programación competitiva (OIE, IOI). Basada en la fuente originale aprende.olimpiada-informatica.org. Cubre análisis de complejidad, técnicas algorítmicas, estructuras de datos y grafos.

## Contexto de Uso

- Resolver problemas de Olimpiadas Informáticas
- Preparación para competencias de programación competitiva
- Aprender análisis de complejidad algorítmica
- Implementar algoritmos eficientes en C++/Python

## Reglas de Uso

1. Siempre analizar complejidad temporal/espacial antes de implementar
2. Preferir complejidad O(log n) sobre O(n) cuando sea posible
3. Considerar el peor caso, no el caso promedio
4. Usar la notación O grande para expresar complejidad
5. Justificar por qué un algoritmo es correcto antes de implementarlo

---

## 1. Fundamentos de Algoritmia

### 1.1 Eficiencia Algorítmica

La **eficiencia** es el aspecto más importante en programación competitiva. Un algoritmo debe ser:

- **Correcto**: Resolver el problema exactamente
- **Eficiente**: Resolverlo dentro de los límites de tiempo y memoria

**Tipos de problemas en OIE/IOI:**
- **Clásicos (batch)**: Programa que dada entrada produce salida
- **Interactivos**: Programa que interactúa con el juez haciendo consultas limitadas
- **Output-only**: Entregar soluciones directamente sin programa

**Ejemplo - Búsqueda Dicotómica (Binary Search):**
- En lugar de buscar secuencialmente O(n), dividir el espacio por la mitad cada vez O(log n)
- Para n=100: máximo 7 preguntas vs 100 preguntas

### 1.2 Análisis de Costes

**Complejidad Temporal (Notación O grande):**

| Complejidad | Nombre | Ejemplo |
|-------------|--------|---------|
| O(1) | Constante | Acceso a array |
| O(log n) | Logarítmica | Binary search |
| O(n) | Lineal | Recorrer array |
| O(n log n) | Lineal-logarítmica | Merge Sort |
| O(n²) | Cuadrática | Bucles anidados |
| O(2^n) | Exponencial | Generación de subconjuntos |
| O(n!) | Factorial | Permutaciones |

**Propiedades:**
- O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2^n) < O(n!)
- Un algoritmo O(n log n) es preferible a O(n²) para entradas grandes
- El factor constante importa menos que el orden de complejidad

**Límites típicos en OIE:**
- 10⁶ operaciones → O(n) aceptable
- 10⁵ operaciones → O(n log n) aceptable
- 10⁴ operaciones → O(n²) puede pasar
- 10³ operaciones → O(n³) aceptable

### 1.3 Análisis de Complejidad - Ejemplos

**Ejemplo 1 - Búsqueda de palabra en texto:**
```cpp
bool buscar(string texto, string palabra) {
    for (int i = 0; i < texto.length(); i++) {
        int j = 0;
        while (j < palabra.length() && texto[i+j] == palabra[j]) j++;
        if (j == palabra.length()) return true;
    }
    return false;
}
```
- Complejidad: O(n × m) donde n = longitud texto, m = longitud palabra
- Peor caso: texto = "AAAA...AAB", palabra = "AAAA...AB"

**Ejemplo 2 - Suma máxima de subarray:**
```cpp
int sumaMaxima(vector<int> v) {
    int max = v[0];
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            int suma = 0;
            for (int k = i; k <= j; k++) suma += v[k];
            if (suma > max) max = suma;
        }
    }
    return max;
}
```
- Complejidad: O(n³)
- Solución óptima: O(n) (Kadane)

**Ejemplo 3 - Binary Search en array ordenado:**
```cpp
int binarySearch(vector<int> v, int x) {
    int l = 0, r = n-1;
    while (l <= r) {
        int m = (l + r) / 2;
        if (v[m] == x) return m;
        else if (v[m] < x) l = m + 1;
        else r = m - 1;
    }
    return -1;
}
```
- Complejidad: O(log n)

### 1.4 Coste de Ordenar

**Teorema:** Todo algoritmo de ordenación basado en comparaciones tiene complejidad Ω(n log n)

**Algoritmos de ordenación:**
- **Selection Sort**: O(n²) - seleccionar mínimo en cada posición
- **Insertion Sort**: O(n²) - insertar elementos en array ordenado
- **Merge Sort**: O(n log n) - divide y vence (recursivo)
- **Quick Sort**: O(n log n) promedio, O(n²) peor caso
- **Counting Sort**: O(n + k) donde k es el rango de valores
- **Radix Sort**: O(nk) donde k es el número de dígitos

**Merge Sort - Implementación:**
```cpp
void mergeSort(vector<int>& v, int l, int r) {
    if (l >= r) return;
    int m = (l + r) / 2;
    mergeSort(v, l, m);
    mergeSort(v, m+1, r);
    merge(v, l, m, r);
}
```
- Divide el problema en subproblemas más pequeños
- Combina las soluciones (O(n) por nivel)
- Total: O(n log n)

---

## 2. Recursividad

Una función recursiva se llama a sí misma. Requiere:
- **Caso base**: Condición de parada
- **Caso recursivo**: Llamada a sí misma con parámetros modificados

**Ejemplos básicos:**

**Contador descendente:**
```cpp
void contador(int n) {
    if (n < 0) return;
    cout << n << endl;
    contador(n-1);
}
```

**Factorial:**
```cpp
int factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n-1);
}
```

**Fibonacci:**
```cpp
int fibonacci(int n) {
    if (n <= 1) return 1;
    return fibonacci(n-1) + fibonacci(n-2);
}
```
- Complejidad naive: O(2^n) - cada llamada genera dos más
- Con memoización: O(n)

**Generar todas las palabras de longitud n:**
```cpp
void generar(string s, int n) {
    if (s.length() == n) {
        cout << s << endl;
        return;
    }
    generar(s + 'a', n);
    generar(s + 'b', n);
}
```
- Total: 2^n palabras generadas

**Patrones Recursivos Comunes:**
- **Divide y vencerás**: Dividir problema, resolver subproblemas, combinar
- **Backtracking**: Explorar todas las opciones, revertir decisiones
- **Inducción**: Asumir solución para n-1, demostrar para n

**Importante:** Siempre tener caso base para evitar recursion infinita y stack overflow.

---

## 3. Algoritmos Voraces (Greedy)

Un algoritmo voraz hace la mejor elección local en cada paso, esperando que lleve a una solución global óptima. No reconsidera decisiones previas.

**Estructura general:**
1. Ordenar/preparar datos según algún criterio
2. Iterar haciendo la mejor elección inmediata
3. Construir la solución final

**Ejemplo 1 - Farolas (Cobertura de puntos):**
```cpp
// Dados M farolas con radio ri en posición yi
// Cubrir N puntos xi con mínimo número de farolas

// Ordenar puntos y farolas
// Para cada punto no cubierto:
//   Elegir farola que lo cubra y llegue más a la derecha
```

- Complejidad: O(N log N + M) con implementación óptima
- Correctitud: demostración por contradicción

**Ejemplo 2 - Cambio de monedas:**
```cpp
int cambio(int cantidad, vector<int> monedas) {
    sort(monedas.rbegin(), monedas.rend()); // mayor a menor
    int resultado = 0;
    for (int m : monedas) {
        resultado += cantidad / m;
        cantidad %= m;
    }
    return resultado;
}
```
- Funciona con monedas de euro (1,2,5,10,20,50,100,200)
- NO funciona con todas las denominaciones (ej: 1,3,4 para cantidad 6)
- Contraejemplo: 6 = 3 + 3 (óptimo) vs 4 + 1 + 1 (greedy)

**Condiciones para que greedy funcione:**
- **Propiedad de elección greedy**: La mejor elección local conduce a la optimalidad global
- **Subestructura óptima**: La solución óptima contiene soluciones óptimas de subproblemas

**Técnica de demostración:**
1. Suponer solución óptima diferente
2. Encontrar primera diferencia con greedy
3. Mostrar que podemos reemplazar sin empeorar
4. Contradicción

---

## 4. Análisis Amortizado

El análisis amortizado calcula el coste promedio de una operación sobre una secuencia de operaciones, garantizando que ninguna operación individual sea demasiado costosa.

**Método agregado:** Calcular el coste total de n operaciones y dividir por n.

**Ejemplo - Array dinámico (similar a vector de C++):**
- Crear array de tamaño 1
- Cuando se llena, crear array del doble tamaño y copiar
- Copiar requiere O(longitud) cuando longitud es potencia de 2

**Análisis:**
- Insertar m elementos
- Número de redimensionamientos: log₂(m) ≈ O(log m)
- Coste total de copias: 1 + 2 + 4 + ... + 2^⌊log₂(m)⌋ = O(m)
- **Complejidad amortizada por inserción: O(1)**

**Aplicaciones comunes:**
- **Dynamic array**: push_back() - O(1) amortizado
- **Stack con array dinámico**: push/pop - O(1) amortizado
- **Cola con dos stacks**: enqueue/dequeue - O(1) amortizado

---

## 5. Algoritmos con Números

### 5.1 Exponenciación Rápida (Binary Exponentiation)

Calcula a^n en O(log n) multiplicaciones:
```
a^n = (a^(n/2))^2              si n es par
a^n = (a^((n-1)/2))^2 * a      si n es impar
```

**Implementación:**
```cpp
long long potencia(long long a, long long n) {
    if (n == 0) return 1;
    long long x = potencia(a, n/2);
    if (n % 2 == 0) return x * x;
    return x * x * a;
}

// Versión iterativa
long long potenciaIter(long long a, long long n) {
    long long resultado = 1;
    while (n > 0) {
        if (n % 2 == 1) resultado *= a;
        a *= a;
        n /= 2;
    }
    return resultado;
}
```

**Exponenciación modular:**
```cpp
long long potenciaMod(long long a, long long n, long long mod) {
    long long resultado = 1;
    a %= mod;
    while (n > 0) {
        if (n % 2 == 1) resultado = (resultado * a) % mod;
        a = (a * a) % mod;
        n /= 2;
    }
    return resultado;
}
```

**Pequeño Teorema de Fermat:**
- Si p es primo y a no divisible por p: a^(p-1) ≡ 1 (mod p)
- Útil para inverso modular: a^(-1) ≡ a^(p-2) (mod p)

### 5.2 Algoritmo de Euclides (GCD)

Calcula el máximo común divisor usando la propiedad:
- gcd(a, b) = gcd(b, a % b)
- gcd(a, 0) = a

**Implementación recursiva:**
```cpp
int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
```

**Implementación iterativa (preferida):**
```cpp
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
```

- Complejidad: O(log min(a, b))

**Propiedades:**
- gcd(a, b) = gcd(a, b-a) (alternativo)
- a × b = gcd(a, b) × lcm(a, b)
- Algoritmo extendido de Euclides: encontrar x, y tales que ax + by = gcd(a, b)

### 5.3 Criba de Eratóstenes

Encuentra todos los primos hasta N en O(N log log N):

```cpp
vector<int> criba(int n) {
    vector<bool> esPrimo(n, true);
    esPrimo[0] = esPrimo[1] = false;
    vector<int> primos;
    
    for (int i = 2; i < n; i++) {
        if (esPrimo[i]) {
            primos.push_back(i);
            // Marcar múltiplos (desde i*i para optimización)
            for (int j = i * i; j < n; j += i)
                esPrimo[j] = false;
        }
    }
    return primos;
}
```

**Optimización clave:** Solo marcar desde i*i porque los múltiplos menores ya fueron marcados por primos más pequeños.

**Complejidad:**
- Número de operaciones: N/2 + N/3 + N/5 + ...
- Suma de inversos de primos ≈ log log N
- Total: O(N log log N)

**Variante segmentada para N muy grande:**
- Dividir en segmentos de tamaño ~√N
- Procesar primos hasta √N primero

### 5.4 Criba de Gries-Misra

Variante más eficiente en memoria para obtener primalidad:

```cpp
vector<int> cribaGries(int n) {
    vector<int> smallestPrimeFactor(n + 1);
    for (int i = 2; i <= n; i++) {
        if (smallestPrimeFactor[i] == 0) {
            smallestPrimeFactor[i] = i;
            if ((long long)i * i <= n) {
                for (int j = i * i; j <= n; j += i) {
                    if (smallestPrimeFactor[j] == 0)
                        smallestPrimeFactor[j] = i;
                }
            }
        }
    }
    return smallestPrimeFactor;
}
```

- Útil para factorización rápida O(log n) por número
- También obtiene lista de primos

---

## 6. Búsqueda Completa y Backtracking

### 6.1 Fundamentos de Búsqueda Completa

Explora todas las posibilidades sistemáticamente hasta encontrar la solución o determinar que no existe.

**Estructura típica:**
```cpp
void backtrack(Estado actual) {
    if (esEstadoFinal(actual)) {
        procesarSolucion(actual);
        return;
    }
    
    for (cada opcion_posible) {
        aplicar(opcion);
        backtrack(nuevo_estado);
        deshacer(opcion); // backtrack
    }
}
```

**Complejidad:** O(b^d) donde b = branching factor, d = profundidad

**Ejemplo - Permutaciones:**
```cpp
void permutar(vector<int>& arr, int idx) {
    if (idx == arr.size()) {
        procesar(arr);
        return;
    }
    for (int i = idx; i < arr.size(); i++) {
        swap(arr[idx], arr[i]);
        permutar(arr, idx + 1);
        swap(arr[idx], arr[i]); // backtrack
    }
}
```

### 6.2 Técnicas de Optimización

**Poda (Pruning):** No explorar ramas que no pueden llevar a solución válida

```cpp
// Ejemplo: Sudoku
if (!esValido(fila, columna, numero)) return; // poda

// Poda por cota inferior (branch and bound)
if (costoActual + costoMinimoEstimado >= mejorSolucion) return;
```

**Ordenamiento heurístico:** Probar opciones más prometedoras primero

**Memoización:** Guardar estados ya visitados para evitar re-explorar

---

## 7. Programación Dinámica

### 7.1 Fundamentos de DP

DP optimiza backtracking eliminando cálculos redundantes almacenando resultados de subproblemas.

**Características:**
1. **Subproblemas superpuestos**: Mismo subproblema aparece múltiples veces
2. **Subestructura óptima**: Solución óptima se construye de soluciones óptimas

**Recurrencia:**
- dp[i] = dp[i-1] + ... (definición del problema)
- dp[i][j] = min/max(dp[i-1][j], dp[i][j-1]) + ... (2D)

### 7.2 Top-Down vs Bottom-Up

**Top-down (recursivo con memoización):**
```cpp
int dp[1000][1000];
int solve(int i, int j) {
    if (i == 0 || j == 0) return 1;
    if (dp[i][j] != -1) return dp[i][j];
    dp[i][j] = solve(i-1, j) + solve(i, j-1);
    return dp[i][j];
}
```

**Bottom-up (iterativo):**
```cpp
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        dp[i][j] = dp[i-1][j] + dp[i][j-1];
    }
}
```

### 7.3 Ejemplos Clásicos

**1. Fibonacci (espacio optimizado):**
```cpp
int fib(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

**2. Subsecuencia común más larga (LCS):**
```cpp
int lcs(string s1, string s2) {
    int n = s1.size(), m = s2.size();
    vector<vector<int>> dp(n+1, vector<int>(m+1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i-1] == s2[j-1])
                dp[i][j] = dp[i-1][j-1] + 1;
            else
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
        }
    }
    return dp[n][m];
}
```

**3. Subarray máximo (Kadane):**
```cpp
int kadane(vector<int> v) {
    int maxActual = v[0], max全局 = v[0];
    for (int i = 1; i < v.size(); i++) {
        maxActual = max(v[i], maxActual + v[i]);
        max全局 = max(max全局, maxActual);
    }
    return max全局;
}
```

**4. Edit Distance:**
```cpp
int editDistance(string s1, string s2) {
    int n = s1.size(), m = s2.size();
    vector<vector<int>> dp(n+1, vector<int>(m+1));
    for (int i = 0; i <= n; i++) dp[i][0] = i;
    for (int j = 0; j <= m; j++) dp[0][j] = j;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i-1] == s2[j-1])
                dp[i][j] = dp[i-1][j-1];
            else
                dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
        }
    }
    return dp[n][m];
}
```

**5. Coin Change (mínimo número de monedas):**
```cpp
int coinChange(vector<int> coins, int amount) {
    vector<int> dp(amount+1, INF);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int c : coins) {
            if (i >= c && dp[i-c] != INF)
                dp[i] = min(dp[i], dp[i-c] + 1);
        }
    }
    return dp[amount] == INF ? -1 : dp[amount];
}
```

### 7.4 SOS DP (Sum Over Subsets)

Calcula valores para todos los subconjuntos en O(n × 2^n):

```cpp
// Para cada mask, calcular suma de f[submask] donde submask ⊆ mask
for (int mask = 0; mask < (1<<n); mask++) {
    dp[mask] = f[mask];
}
for (int i = 0; i < n; i++) {
    for (int mask = 0; mask < (1<<n); mask++) {
        if (mask & (1<<i)) {
            dp[mask] += dp[mask ^ (1<<i)];
        }
    }
}
```

**Aplicaciones:**
- Contar subconjuntos con suma dada
- DP sobre subconjuntos de bits

### 7.5 Optimizaciones de DP

**1. Conversión 1D a 2D con espacio:**
```cpp
// 2D: O(n*m) espacio
// 1D: O(m) espacio, iterando en orden correcto
for (int i = 1; i <= n; i++) {
    for (int j = m; j >= 0; j--) {
        dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
    }
}
```

**2. Monotonic Queue (DP con optimización convexa):**
- Para dp[i] = min(dp[j] + cost(j, i)) con j < i
- Aplicable cuando cost tiene estructura específica

**3. Divide and Conquer DP:**
- Para dp[i] = min(dp[j] + C(j, i)) donde C cumple quadrangle inequality
- Complejidad: O(n log n) o O(n)

---

## 8. Estructuras de Datos STL (C++)

### 8.1 Pilas y Colas

**Stack (LIFO):**
```cpp
stack<int> s;
s.push(1);      // O(1)
s.top();       // O(1)
s.pop();       // O(1)
s.empty();     // O(1)
```

**Queue (FIFO):**
```cpp
queue<int> q;
q.push(1);
q.front();     // O(1)
q.pop();
q.empty();
```

**Deque (double-ended queue):**
```cpp
deque<int> d;
d.push_front(1);
d.push_back(2);
d.front(); d.back();
```

### 8.2 Mapas y Sets

**Unordered Map (tabla hash):**
```cpp
unordered_map<string, int> um;
um["clave"] = valor;      // O(1) promedio
um.find("clave");         // O(1)
um.erase("clave");
```

**Unordered Set:**
```cpp
unordered_set<int> us;
us.insert(1);
us.find(2);
us.erase(3);
```

**Map (árbol equilibrado - O(log n)):**
```cpp
map<string, int> m;
m["a"] = 1;
m.insert({"b", 2});
auto it = m.lower_bound("a");
```

**Set:**
```cpp
set<int> s;
s.insert(5);
s.find(5);
s.erase(5);
```

**Multimap/Multiset (claves duplicadas):**
```cpp
multimap<string, int> mm;
mm.insert({"clave", 1});
mm.insert({"clave", 2});
```

### 8.3 Priority Queue (Heap)

```cpp
priority_queue<int> maxHeap;           // Mayor arriba
priority_queue<int, vector<int>, greater<int>> minHeap;

// Estructura con comparación personalizada
struct Node {
    int valor, prioridad;
    bool operator<(const Node& other) const {
        return prioridad < other.prioridad;
    }
};
priority_queue<Node> pq;
```

**Operaciones:** O(log n)
- push()
- top()
- pop()
- empty()

---

## 9. Estructuras de Datos Custom

### 9.1 RSQ y Sumas Acumulativas (Prefix Sum)

Para consultas de suma en rango [l, r]:

```cpp
class PrefixSum {
    vector<long long> ps;
public:
    PrefixSum(const vector<int>& arr) {
        ps.resize(arr.size() + 1);
        ps[0] = 0;
        for (int i = 0; i < arr.size(); i++)
            ps[i+1] = ps[i] + arr[i];
    }
    long long query(int l, int r) {
        return ps[r+1] - ps[l];
    }
};
```
- Construcción: O(n)
- Consulta: O(1)
- Actualización: O(n) (reconstruir)

### 9.2 RMQ y Sparse Table

Range Minimum Query - consultar mínimo en rango:

```cpp
class SparseTable {
    vector<vector<int>> st;
    vector<int> log2;
public:
    SparseTable(const vector<int>& arr) {
        int n = arr.size();
        log2.resize(n+1);
        for (int i = 2; i <= n; i++) log2[i] = log2[i/2] + 1;
        
        int K = log2[n] + 1;
        st.assign(K, vector<int>(n));
        st[0] = arr;
        
        for (int k = 1; k < K; k++) {
            for (int i = 0; i + (1<<k) <= n; i++) {
                st[k][i] = min(st[k-1][i], st[k-1][i + (1<<(k-1))]);
            }
        }
    }
    
    int query(int l, int r) {
        int k = log2[r - l + 1];
        return min(st[k][l], st[k][r - (1<<k) + 1]);
    }
};
```
- Construcción: O(n log n)
- Consulta: O(1)
- Espacio: O(n log n)

### 9.3 Árbol de Segmentos (Segment Tree)

Permite consultas y actualizaciones en rango:

```cpp
class SegTree {
    vector<int> tree;
    int n;
public:
    SegTree(const vector<int>& arr) {
        n = arr.size();
        tree.assign(4*n, 0);
        build(1, 0, n-1, arr);
    }
    
    void build(int node, int l, int r, const vector<int>& arr) {
        if (l == r) { tree[node] = arr[l]; return; }
        int m = (l+r)/2;
        build(2*node, l, m, arr);
        build(2*node+1, m+1, r, arr);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    void update(int idx, int val) { update(1, 0, n-1, idx, val); }
    void update(int node, int l, int r, int idx, int val) {
        if (l == r) { tree[node] = val; return; }
        int m = (l+r)/2;
        if (idx <= m) update(2*node, l, m, idx, val);
        else update(2*node+1, m+1, r, idx, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    int query(int ql, int qr) { return query(1, 0, n-1, ql, qr); }
    int query(int node, int l, int r, int ql, int qr) {
        if (qr < l || ql > r) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int m = (l+r)/2;
        return query(2*node, l, m, ql, qr) + query(2*node+1, m+1, r, ql, qr);
    }
};
```
- Construcción: O(n)
- Consulta: O(log n)
- Update: O(log n)

**Variantes:**
- Lazy propagation para updates de rango
- Segmentos persistentes para versiones
- Binary lifting (walking) para encontrar primer índice

### 9.4 Union-Find (Disjoint Set Union - DSU)

Estructura para mantener componentes conectados:

```cpp
class DSU {
    vector<int> parent, rank;
public:
    DSU(int n) {
        parent.resize(n);
        rank.assign(n, 0);
        iota(parent.begin(), parent.end(), 0);
    }
    
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]); // path compression
        return parent[x];
    }
    
    void unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return;
        if (rank[a] < rank[b]) swap(a, b);
        parent[b] = a;
        if (rank[a] == rank[b]) rank[a]++;
    }
};
```
- find: O(α(n)) ≈ O(1) amortizado
- unite: O(α(n)) amortizado
- α(n) es la función de Ackermann inverso

### 9.5 Descomposición SQRT (Mo's Algorithm)

Para consultas offline en rangos:

```cpp
struct Query {
    int l, r, idx, block;
    bool operator<(const Query& other) const {
        if (block != other.block) return block < other.block;
        return (block % 2) ? r > other.r : r < other.r;
    }
};

vector<int> respuesta;
int currentL = 0, currentR = -1;

void add(int position) { /* actualizar estructura */ }
void remove(int position) { /* actualizar estructura */ }

void solveQueries(vector<Query> queries) {
    sort(queries.begin(), queries.end());
    for (auto q : queries) {
        while (currentL > q.l) add(--currentL);
        while (currentR < q.r) add(++currentR);
        while (currentL < q.l) remove(currentL++);
        while (currentR > q.r) remove(currentR--);
        respuesta[q.idx] = getAnswer();
    }
}
```
- Complejidad: O((n + q) × √n)

### 9.6 Trie (Árbol de Prefijos)

Estructura para cadenas:

```cpp
struct TrieNode {
    array<int, 26> next;
    bool isEnd;
    TrieNode() {
        next.fill(-1);
        isEnd = false;
    }
};

class Trie {
    vector<TrieNode> nodes;
public:
    Trie() { nodes.push_back(TrieNode()); }
    
    void insert(string s) {
        int node = 0;
        for (char c : s) {
            int idx = c - 'a';
            if (nodes[node].next[idx] == -1) {
                nodes[node].next[idx] = nodes.size();
                nodes.push_back(TrieNode());
            }
            node = nodes[node].next[idx];
        }
        nodes[node].isEnd = true;
    }
    
    bool find(string s) {
        int node = 0;
        for (char c : s) {
            int idx = c - 'a';
            if (nodes[node].next[idx] == -1) return false;
            node = nodes[node].next[idx];
        }
        return nodes[node].isEnd;
    }
};
```
- Inserción/Búsqueda: O(|s|)
- Espacio: O(|s| × número de strings)

### 9.7 Treap (BST aleatorizado)

BST con rotación automática:

```cpp
struct Node {
    int key, priority;
    Node *left, *right;
    Node(int k) : key(k), priority(rand()), left(nullptr), right(nullptr) {}
};

class Treap {
    Node* root = nullptr;
    
    Node* rotateRight(Node* y) {
        Node* x = y->left;
        y->left = x->right;
        x->right = y;
        return x;
    }
    
    Node* rotateLeft(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        y->left = x;
        return y;
    }
    
    Node* insert(Node* node, int key) {
        if (!node) return new Node(key);
        if (key < node->key) {
            node->left = insert(node->left, key);
            if (node->left->priority < node->priority)
                node = rotateRight(node);
        } else {
            node->right = insert(node->right, key);
            if (node->right->priority < node->priority)
                node = rotateLeft(node);
        }
        return node;
    }
};
```
- Complejidad esperada: O(log n)
- Equilibrio garantizado por prioridades aleatorias

### 9.8 Li Chao Tree

Segment tree para líneas (convexo hull trick):

```cpp
struct Line {
    long long m, b; // y = mx + b
    long long eval(long long x) { return m*x + b; }
};

class LiChao {
    struct Node {
        Line line;
        Node *left, *right;
        Node(Line l) : line(l), left(nullptr), right(nullptr) {}
    };
    Node* root = nullptr;
    long long X_MIN, X_MAX;
    
    void addLine(Line newLine, Node*& node, long long l, long long r) {
        if (!node) { node = new Node(newLine); return; }
        
        long long mid = (l + r) / 2;
        bool leftBetter = newLine.eval(l) < node->line.eval(l);
        bool midBetter = newLine.eval(mid) < node->line.eval(mid);
        
        if (midBetter) {
            swap(node->line, newLine);
        }
        
        if (r - l == 1) return;
        
        if (leftBetter != midBetter)
            addLine(newLine, node->left, l, mid);
        else
            addLine(newLine, node->right, mid, r);
    }
    
    long long query(long long x, Node* node, long long l, long long r) {
        if (!node) return LLONG_MAX;
        long long res = node->line.eval(x);
        if (r - l == 1) return res;
        long long mid = (l + r) / 2;
        if (x < mid) return min(res, query(x, node->left, l, mid));
        return min(res, query(x, node->right, mid, r));
    }
};
```
- Insertar línea: O(log C) donde C es rango de x
- Query: O(log C)

---

## 10. Grafos

### 10.1 Representación de Grafos

**Lista de adyacencia (preferida):**
```cpp
vector<vector<int>> adj(n); // para grafo no pesado
vector<vector<pair<int,int>>> adj(n); // para grafo con pesos
```

**Matriz de adyacencia:**
```cpp
int adj[n][n]; // para grafos densos
```

### 10.2 Graph Traversal (DFS y BFS)

**DFS - Depth First Search:**
```cpp
void dfs(int u, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs(v, adj, visited);
    }
}
```

**BFS - Breadth First Search:**
```cpp
void bfs(int start, vector<vector<int>>& adj) {
    vector<bool> visited(adj.size());
    queue<int> q;
    q.push(start);
    visited[start] = true;
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
}
```

**Aplicaciones:**
- DFS: componentes conexas, topological sort, detección de ciclos
- BFS: camino más corto en grafo no pesado, niveles

### 10.3 Caminos Más Cortos

**Dijkstra (grafos con pesos no negativos):**
```cpp
vector<long long> dijkstra(int src, vector<vector<pair<int,int>>>& adj) {
    int n = adj.size();
    vector<long long> dist(n, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
    dist[src] = 0;
    pq.push({0, src});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```
- Complejidad: O((V+E) log V)
- Solo funciona con pesos no negativos

**Bellman-Ford (pesos pueden ser negativos):**
```cpp
vector<long long> bellmanFord(int src, vector<vector<pair<int,int>>>& adj, int V) {
    vector<long long> dist(V, LLONG_MAX);
    dist[src] = 0;
    for (int i = 0; i < V-1; i++) {
        for (auto& [u, edges] : enumerate(adj)) {
            for (auto [v, w] : edges) {
                if (dist[u] != LLONG_MAX && dist[u] + w < dist[v])
                    dist[v] = dist[u] + w;
            }
        }
    }
    return dist;
}
```
- Complejidad: O(V × E)
- Detecta ciclos negativos

**Floyd-Warshall (todos los pares):**
```cpp
vector<vector<long long>> floydWarshall(vector<vector<long long>>& dist, int V) {
    for (int k = 0; k < V; k++)
        for (int i = 0; i < V; i++)
            for (int j = 0; j < V; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
    return dist;
}
```
- Complejidad: O(V³)
- Funciona con pesos negativos (sin ciclos negativos)

### 10.4 Minimum Spanning Tree (MST)

**Kruskal:**
```cpp
struct Edge { int u, v, w; };
vector<Edge> edges;
sort(edges.begin(), edges.end(), [](Edge a, Edge b){ return a.w < b.w; });

DSU dsu(V);
vector<Edge> mst;
for (auto e : edges) {
    if (dsu.find(e.u) != dsu.find(e.v)) {
        dsu.unite(e.u, e.v);
        mst.push_back(e);
    }
}
```
- Complejidad: O(E log E) = O(E log V)

**Prim:**
```cpp
vector<bool> visited(V, false);
priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
pq.push({0, 0}); // (peso, nodo)
long long mst = 0;
while (!pq.empty()) {
    auto [w, u] = pq.top(); pq.pop();
    if (visited[u]) continue;
    visited[u] = true;
    mst += w;
    for (auto [v, w2] : adj[u]) {
        if (!visited[v]) pq.push({w2, v});
    }
}
```
- Complejidad: O(E log V)

### 10.5 Componentes Conexas y Bicoloración

**DFS para componentes:**
```cpp
void findComponents() {
    vector<int> component(V, -1);
    int compId = 0;
    for (int i = 0; i < V; i++) {
        if (component[i] == -1) {
            dfs(i, compId++, component);
        }
    }
}
```

**Bipartite check (bicoloración):**
```cpp
bool isBipartite() {
    vector<int> color(V, -1);
    for (int i = 0; i < V; i++) {
        if (color[i] == -1) {
            color[i] = 0;
            queue<int> q; q.push(i);
            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (int v : adj[u]) {
                    if (color[v] == -1) {
                        color[v] = 1 - color[u];
                        q.push(v);
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
}
```

### 10.6 Árbol DFS, Puentes y Puntos de Articulación

**Puentes:** Aristas cuya eliminación aumenta componentes

**Puntos de articulación:** Vértices cuya eliminación desconecta el grafo

```cpp
void findBridgesAP() {
    vector<int> tin(V, -1), low(V, -1);
    vector<bool> visited(V, false);
    vector<pair<int,int>> bridges;
    vector<int> articulation;
    int timer = 0;
    
    function<void(int,int)> dfs = [&](int v, int p) {
        visited[v] = true;
        tin[v] = low[v] = timer++;
        int children = 0;
        for (int to : adj[v]) {
            if (to == p) continue;
            if (visited[to]) {
                low[v] = min(low[v], tin[to]);
            } else {
                children++;
                dfs(to, v);
                low[v] = min(low[v], low[to]);
                if (low[to] > tin[v])
                    bridges.push_back({v, to});
                if (p != -1 && low[to] >= tin[v])
                    articulation.push_back(v);
            }
        }
        if (p == -1 && children > 1)
            articulation.push_back(v);
    };
}
```

### 10.7 SCC y 2-SAT

**Strongly Connected Components (Kosaraju):**
1. DFS para obtener orden topológico inverso
2. Invertir grafo
3. DFS en orden inverso para obtener SCCs

```cpp
void kosaraju() {
    // Paso 1: orden topológico
    for (int i = 0; i < V; i++)
        if (!visited[i]) dfs1(i);
    
    // Paso 2: procesar en orden inverso
    fill(visited.begin(), visited.end(), false);
    for (int i = V-1; i >= 0; i--)
        if (!visited[order[i]]) {
            dfs2(order[i], compId++);
        }
}
```

**2-SAT:** Problema de satisfacibilidad booleana con cláusulas de 2 literales

```cpp
// Resolver (a OR b) AND (!a OR c) AND ...
// Crear grafo de implicaciones
// SCC donde x y !x están en diferentes SCCs = satisfacible
```

### 10.8 LCA (Lowest Common Ancestor)

**Binary Lifting:**
```cpp
const int LOG = 20;
vector<vector<int>> up(LOG, vector<int>(V));
vector<int> depth(V);

void dfs(int v, int p) {
    up[0][v] = p;
    for (int i = 1; i < LOG; i++)
        up[i][v] = up[i-1][ up[i-1][v] ];
    for (int to : adj[v])
        if (to != p) {
            depth[to] = depth[v] + 1;
            dfs(to, v);
        }
}

int lca(int a, int b) {
    if (depth[a] < depth[b]) swap(a, b);
    int diff = depth[a] - depth[b];
    for (int i = 0; i < LOG; i++)
        if (diff & (1<<i)) a = up[i][a];
    if (a == b) return a;
    for (int i = LOG-1; i >= 0; i--) {
        if (up[i][a] != up[i][b]) {
            a = up[i][a];
            b = up[i][b];
        }
    }
    return up[0][a];
}
```

### 10.9 HLD (Heavy Light Decomposition)

Descomponer árbol en rutas para consultas de rango en árbol:

```cpp
// 1. Identificar hijo pesado
// 2. Asignar posición en DFS
// 3. Consultar en O(log² n) usando segment tree
```

### 10.10 Flow Algorithms

**Ford-Fulkerson / Edmonds-Karp:**
```cpp
int maxFlow(int s, int t) {
    int flow = 0;
    while (bfs(s, t, parent)) {
        int pathFlow = INF;
        for (int v = t; v != s; v = parent[v])
            pathFlow = min(pathFlow, capacity[parent[v]][v]);
        flow += pathFlow;
        for (int v = t; v != s; v = parent[v]) {
            capacity[parent[v]][v] -= pathFlow;
            capacity[v][parent[v]] += pathFlow;
        }
    }
    return flow;
}
```

---

## 11. Geometría Computacional

### 11.1 Operaciones Básicas

**Punto y vector:**
```cpp
struct Point {
    double x, y;
    Point operator+(Point p) { return {x + p.x, y + p.y}; }
    Point operator-(Point p) { return {x - p.x, y - p.y}; }
    double operator*(Point p) { return x*p.x + y*p.y; } // producto punto
    double cross(Point p) { return x*p.y - y*p.x; } // producto cruz
};
```

**Distancia:** |AB| = √((x₂-x₁)² + (y₂-y₁)²)

### 11.2 Algoritmos Comunes

**Convex Hull (Graham scan):**
```cpp
vector<Point> convexHull(vector<Point> pts) {
    sort(pts.begin(), pts.end());
    vector<Point> lower, upper;
    for (auto p : pts) {
        while (lower.size() >= 2 && 
               cross(lower[lower.size()-2], lower.back(), p) <= 0)
            lower.pop_back();
        lower.push_back(p);
    }
    for (int i = pts.size()-1; i >= 0; i--) {
        while (upper.size() >= 2 && 
               cross(upper[upper.size()-2], upper.back(), pts[i]) <= 0)
            upper.pop_back();
        upper.push_back(pts[i]);
    }
    lower.pop_back(); upper.pop_back();
    return lower; // concatenated
}
```

**Detección de intersección de segmentos:**
- Comparar orientaciones
- Check general case y special cases

**Área de polígono:**
```cpp
double area(const vector<Point>& poly) {
    double a = 0;
    for (int i = 0; i < poly.size(); i++) {
        int j = (i + 1) % poly.size();
        a += poly[i].cross(poly[j]);
    }
    return abs(a) / 2;
}
```

---

## 12. Técnicas Avanzadas

### 12.1 Búsqueda Dicotómica

**Binary search en valor:**
```cpp
int busqueda(int l, int r) {
    while (l < r) {
        int m = (l + r) / 2;
        if (cond(m)) r = m;
        else l = m + 1;
    }
    return l;
}
```

**Binary search en respuesta:**
```cpp
int buscarRespuesta(int maximo) {
    int l = 0, r = maximo;
    while (l < r) {
        int m = (l + r) / 2;
        if (esFactible(m)) r = m;
        else l = m + 1;
    }
    return l;
}
```

### 12.2 Two Pointers

```cpp
// Para encontrar pares con suma objetivo en array ordenado
int i = 0, j = n-1;
while (i < j) {
    if (a[i] + a[j] == target) { /* found */ i++; j--; }
    else if (a[i] + a[j] < target) i++;
    else j--;
}
```

### 12.3 Meet in the Middle

Para problemas con búsqueda exhaustiva:
- Dividir en dos mitades
- Resolver cada mitad independientemente
- Combinar resultados

```cpp
// Ejemplo: subconjunto que suma S de n elementos (n ≤ 40)
// Dividir en dos grupos de n/2
// Generar todas las sums de cada mitad (2^(n/2) cada una)
// Buscar pares que sumen S
```

---

## 13. Complejidades de Referencia

### Estructuras de Datos

| Estructura | Access | Search | Insert | Delete |
|------------|--------|--------|--------|--------|
| Array | O(1) | O(n) | - | - |
| Linked List | O(n) | O(n) | O(1)* | O(1)* |
| Stack | - | - | O(1) | O(1) |
| Queue | - | - | O(1) | O(1) |
| Hash Table | - | O(1) avg | O(1) avg | O(1) avg |
| BST | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | - | O(1) | O(log n) | O(log n) |
| Segment Tree | O(log n) | O(log n) | O(log n) | O(log n) |

### Algoritmos de Grafos

| Algoritmo | Complejidad | Restricciones |
|-----------|-------------|---------------|
| BFS/DFS | O(V + E) | - |
| Dijkstra | O((V+E) log V) | Pesos ≥ 0 |
| Bellman-Ford | O(VE) | Sin ciclos neg |
| Floyd-Warshall | O(V³) | - |
| Kruskal | O(E log V) | - |
| Prim | O(E log V) | - |
| Kosaraju | O(V + E) | - |

### Algoritmos de Ordenación

| Algoritmo | Tiempo | Espacio |
|-----------|--------|---------|
| Selection | O(n²) | O(1) |
| Insertion | O(n²) | O(1) |
| Merge | O(n log n) | O(n) |
| Heap | O(n log n) | O(1) |
| Quick | O(n log n)* | O(1) |
| Counting | O(n + k) | O(k) |

---

## 14. Consejos para Competiciones

1. **Leer todos los problemas** antes de empezar a codear
2. **Calcular complejidad** antes de implementar
3. **Testing local** con casos edge y aleatorios
4. **Debugging**: usar assert, prints limitados
5. **Tiempo**: 30% lectura, 40% diseño, 30% implementación
6. **No optimizaciones prematuras**: primero correctness, luego eficiencia
7. **Practicar temas弱势**: weaker areas
8. **Estudiar soluciones** de problemas anteriores

---

## Problemas de Práctica por Tema

- **Búsqueda dicotómica**: buscar en array ordenado, buscar respuesta
- **Backtracking**: N-reinas, Sudoku, generación de subconjuntos
- **DP**: LCS, knapsack, edit distance, subarray máximo
- **Grafos**: BFS/DFS, Dijkstra, componentes conexas
- **Estructuras**: segment tree, union-find
- **Números**: primalidad, GCD, exponenciación modular

---

## 15. Guía de Decisión: ¿Qué Técnica Uso?

Esta matriz te ayuda a elegir la técnica correcta según la forma del problema. Siempre empezá mirando los límites (N) y el tipo de consulta.

### 15.1 Por tamaño de entrada (N)

| N máximo | Complejidad permitida | Técnicas candidatas |
|----------|----------------------|---------------------|
| N ≤ 11 | O(N!) | Backtracking puro, permutaciones |
| N ≤ 20 | O(2^N), O(2^N × N) | Bitmask DP, Meet in the middle (hasta 40) |
| N ≤ 40 | O(2^(N/2)) | Meet in the middle |
| N ≤ 100 | O(N⁴) | DP 2D con estados compuestos, Floyd-Warshall |
| N ≤ 500 | O(N³) | DP cúbica, Floyd-Warshall |
| N ≤ 5000 | O(N²) | DP cuadrática, programación dinámica clásica |
| N ≤ 10⁵ | O(N log N) | Sort, segment tree, Dijkstra, binary search |
| N ≤ 10⁶ | O(N) o O(N log log N) | Two pointers, Kadane, criba, DSU |
| N ≤ 10⁸ | O(log N) o O(√N) | Exponenciación rápida, raíz cuadrada |
| N ≤ 10¹⁸ | O(log N) o O(1) | Math, exponenciación modular |

### 15.2 Por forma del problema

| Problema dice... | Técnica típica |
|------------------|----------------|
| "mínimo/máximo número de..." | DP o Greedy |
| "cuántas formas de..." | DP de conteo, combinatoria |
| "¿existe un camino?" | BFS/DFS |
| "camino más corto con pesos ≥ 0" | Dijkstra |
| "camino más corto con pesos negativos" | Bellman-Ford |
| "todos los pares de distancias" | Floyd-Warshall |
| "conectar todo con costo mínimo" | MST (Kruskal/Prim) |
| "agrupar/unir elementos" | DSU |
| "consultas de rango + updates" | Segment Tree |
| "consultas de rango sin updates" | Prefix Sum / Sparse Table |
| "buscar valor mínimo que cumple X" | Binary search en respuesta |
| "el orden importa" | Permutaciones, DP con estado de orden |
| "el orden no importa" | Combinatoria, subsets |
| "subcadena/subsecuencia" | DP 2D (LCS, Edit Distance) |
| "prefijos/palabras" | Trie |
| "calcular a^n mod p" | Exponenciación rápida modular |

---

## 16. Puentes Entre Temas (Cómo Combinar Técnicas)

Los problemas reales casi nunca usan una sola técnica. Aquí están las combinaciones más frecuentes en OIE/IOI.

### 16.1 Binary Search + otra cosa

- **Binary Search + Greedy**: "Minimizar el máximo" — buscás el valor máximo X tal que una estrategia greedy lo logre. Ejemplo: repartir tareas entre K workers minimizando el tiempo del más cargado.
- **Binary Search + DP**: Parametrizás el DP por el valor buscado. Ejemplo: LIS en O(N log N) usando búsqueda binaria sobre el array de menores finales.
- **Binary Search + Grafos**: Buscás el peso máximo de arista en el camino más corto. Ejemplo: "path con bottleneck mínimo".

### 16.2 DP + otra cosa

- **DP + Bitmask**: Cuando N ≤ 20. Estado = subconjunto de elementos ya procesados. Ejemplo: TSP en O(2^N × N²).
- **DP + Grafos (DAG)**: Si el grafo es acíclico, podés hacer DP sobre el orden topológico. Ejemplo: camino más largo en DAG.
- **DP + Árboles**: DP sobre subárboles. Cada nodo agrega información de sus hijos. Ejemplo: tamaño de cada subárbol, distancia máxima en árbol.
- **DP + Segment Tree**: Cuando la recurrencia necesita consultar un rango de estados anteriores. Ejemplo: LIS con queries de rango.
- **DP + Convex Hull Trick**: Cuando la recurrencia tiene forma `dp[i] = min(dp[j] + a[j]×x[i] + b[j])`.

### 16.3 Grafos + DSU

- **MST (Kruskal)**: Ordenás aristas y usás DSU para detectar ciclos. Caso de uso clásico.
- **Conectividad offline**: Procesás queries ordenándolas por tiempo y uniendo componentes con DSU.
- **Kruskal reconstructivo**: Construís un árbol binario que representa el proceso de unión. Útil para queries de "peso máximo en el camino".

### 16.4 Segment Tree + otra cosa

- **Segment Tree + Lazy Propagation**: Updates de rango. Ejemplo: sumar X a todo un rango, consultar suma.
- **Segment Tree + Coordinate Compression**: Cuando los índices son muy grandes pero pocos distintos.
- **Merge Sort Tree**: Segment tree donde cada nodo guarda un vector ordenado. Para queries como "cuántos elementos menores a K en [l, r]".

### 16.5 Combinaciones clásicas de OIE

- **Dijkstra modificado**: Estado = (nodo, info extra). Ejemplo: shortest path con K teletransportes.
- **BFS 0-1**: Aristas con peso 0 o 1. Usás deque en vez de priority queue → O(V+E).
- **Multi-source BFS**: Arrancás BFS desde múltiples nodos a la vez. Ejemplo: distancia al hospital más cercano.
- **Two Pointers + Sliding Window**: Subarray con propiedad. Ejemplo: subarray más largo con suma ≤ K.
- **Prefix Sum + Hash Map**: "Cuántos subarrays tienen suma X" en O(N).

---

## 17. Casos de Uso Concretos (Problemas Clásicos Resueltos)

### 17.1 Caso: "Dividir array en K partes minimizando la máxima suma"

**Problema**: Array de N números, dividir en K subarrays contiguos. Minimizar la suma máxima entre subarrays.

**Técnica**: Binary Search en respuesta + Greedy

```cpp
bool puedeDividir(vector<int>& arr, int K, long long maxSuma) {
    int grupos = 1;
    long long actual = 0;
    for (int x : arr) {
        if (x > maxSuma) return false;
        if (actual + x > maxSuma) { grupos++; actual = x; }
        else actual += x;
    }
    return grupos <= K;
}

long long resolver(vector<int>& arr, int K) {
    long long l = *max_element(arr.begin(), arr.end());
    long long r = accumulate(arr.begin(), arr.end(), 0LL);
    while (l < r) {
        long long m = (l + r) / 2;
        if (puedeDividir(arr, K, m)) r = m;
        else l = m + 1;
    }
    return l;
}
```

**Por qué funciona**: Si podés dividir con suma máxima X, podés con X+1. Función monótona → binary search.

### 17.2 Caso: "Camino más corto con paradas obligatorias"

**Problema**: Grafo con pesos, encontrar shortest path de A a B que pase por los nodos `{v1, v2, ..., vk}` en cualquier orden.

**Técnica**: Dijkstra + Bitmask DP (cuando k es pequeño, k ≤ 15)

```cpp
// dist[nodo][mask] = distancia mínima llegando a 'nodo'
// habiendo visitado los nodos en 'mask'
// Dijkstra sobre estados (nodo, mask)
```

**Por qué funciona**: El estado combinado captura tanto la posición como el conjunto visitado.

### 17.3 Caso: "¿Hay ciclo en el grafo?"

**Técnicas según el tipo**:

- **Grafo no dirigido**: DFS y chequear si visitás un nodo ya visitado que no sea el padre. O DSU: si al unir dos nodos ya están conectados, hay ciclo.
- **Grafo dirigido**: DFS con 3 colores (blanco/gris/negro). Si llegás a un nodo gris, hay ciclo.
- **Detección temprana**: Topological sort con Kahn. Si no podés ordenar todos los nodos, hay ciclo.

### 17.4 Caso: "Subarray con suma exactamente K"

**Técnica**: Prefix Sum + Hash Map

```cpp
int contarSubarrays(vector<int>& arr, int K) {
    unordered_map<long long, int> cnt;
    cnt[0] = 1;
    long long suma = 0;
    int res = 0;
    for (int x : arr) {
        suma += x;
        if (cnt.count(suma - K)) res += cnt[suma - K];
        cnt[suma]++;
    }
    return res;
}
```

**Por qué funciona**: Si `prefix[j] - prefix[i] = K`, entonces el subarray (i, j] suma K. Buscás cuántos prefix anteriores cumplen `prefix[i] = prefix[j] - K`.

### 17.5 Caso: "N-Reinas"

**Técnica**: Backtracking con poda

```cpp
int n, soluciones = 0;
vector<bool> col, diag1, diag2;

void backtrack(int fila) {
    if (fila == n) { soluciones++; return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[fila+c] || diag2[fila-c+n]) continue;
        col[c] = diag1[fila+c] = diag2[fila-c+n] = true;
        backtrack(fila + 1);
        col[c] = diag1[fila+c] = diag2[fila-c+n] = false;
    }
}
```

**Por qué funciona**: Las restricciones (columna, diagonal) se chequean en O(1) con arrays booleanos. Poda agresiva.

### 17.6 Caso: "Queries de conectividad offline"

**Problema**: N nodos, M operaciones del tipo: "conectar u con v" o "¿están u y v conectados?". Procesar todo en orden.

**Técnica**: DSU (Union-Find)

**Por qué**: Cada operación es O(α(N)) ≈ O(1). Total O((N+M) α(N)).

### 17.7 Caso: "Encontrar el k-ésimo más pequeño en un stream"

**Técnica**: Two heaps (max-heap + min-heap) o multiset

```cpp
// Para mediana: max-heap con la mitad inferior, min-heap con la superior
priority_queue<int> lo;
priority_queue<int, vector<int>, greater<int>> hi;

void add(int x) {
    lo.push(x);
    hi.push(lo.top()); lo.pop();
    if (lo.size() < hi.size()) { lo.push(hi.top()); hi.pop(); }
}
double mediana() {
    return lo.size() > hi.size() ? lo.top() : (lo.top() + hi.top()) / 2.0;
}
```

---

## 18. Errores Comunes y Cómo Evitarlos

1. **Overflow**: Usar `long long` cuando la suma pueda exceder 2×10⁹. Multiplicaciones con `int` explotan a los 46000².
2. **Integer division**: `(a + b) / 2` puede overflow. Mejor: `a + (b - a) / 2`.
3. **Off-by-one en binary search**: Decidir si `r = m` o `r = m - 1` según si la condición es "primer true" o "último true".
4. **Stack overflow en DFS recursivo**: Para N grande (> 10⁵), convertir a iterativo con stack explícito.
5. **Modular inverse con números no coprimos**: Fermat solo funciona si el módulo es primo y el número no es múltiplo.
6. **Olvidar el caso base en recursión**: Siempre escribilo primero.
7. **Priority queue con floats**: Cuidado con comparaciones de igualdad, usar `abs(a-b) < EPS`.
8. **DSU sin path compression**: Complejidad se degrada a O(log N) por operación. Siempre usar ambas optimizaciones.
9. **Segment tree con array de tamaño `2*n`**: Necesitás `4*n` para cubrir todos los casos.
10. **Dijkstra con pesos negativos**: No funciona. Usá Bellman-Ford.

---

## 19. Plantillas Rápidas para Competencia

### Template base C++

```cpp
#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define pb push_back
#define all(x) (x).begin(), (x).end()
#define sz(x) (int)(x).size()

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    // solución
    
    return 0;
}
```

### Lectura rápida

```cpp
// Para I/O pesado
ios_base::sync_with_stdio(false);
cin.tie(NULL);
// O usar scanf/printf directamente
```

### Constantes útiles

```cpp
const int INF = 1e9;
const ll INFLL = 1e18;
const int MOD = 1e9 + 7;
const double EPS = 1e-9;
```