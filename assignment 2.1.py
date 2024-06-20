import math


# Define functions
def func1(x):
    return x ** 31 - 1000


def func2(x):
    return math.sin(x)**5 * math.cos(x)**3 - math.exp(x)


def func3(x):
    return 1/(1+ math.exp(-x**2 - math.sin(x)-x)) - 1/2


# Finite difference method for estimating derivatives
def finite_difference_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h


# Bisection Method
def bisection_method(func, a, b, tol=1e-3, max_iter=1000):
    if func(a) * func(b) >= 0:
        return None, max_iter
    iter_count = 0
    while (b - a) / 2.0 > tol and iter_count < max_iter:
        midpoint = (a + b) / 2.0
        if func(midpoint) == 0:
            return midpoint, iter_count
        elif func(a) * func(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint
        iter_count += 1
    return (a + b) / 2.0, iter_count


# Newton-Raphson Method
def newton_raphson_method(func, x0, tol=1e-3, max_iter=1000):
    iter_count = 0
    while iter_count < max_iter:
        fx = func(x0)
        if abs(fx) < tol:
            return x0, iter_count
        dfx = finite_difference_derivative(func, x0)
        if dfx == 0:
            return None, max_iter
        x0 = x0 - fx / dfx
        iter_count += 1
    return x0, iter_count


# Secant Method
def secant_method(func, x0, x1, tol=1e-3, max_iter=1000):
    iter_count = 0
    while iter_count < max_iter:
        fx0 = func(x0)
        fx1 = func(x1)
        if abs(fx1) < tol:
            return x1, iter_count
        if fx1 - fx0 == 0:
            return None, max_iter
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x2
        iter_count += 1
    return x1, iter_count


# Regula Falsi Method
def regula_falsi_method(func, a, b, tol=1e-3, max_iter=1000):
    if func(a) * func(b) >= 0:
        return None, max_iter
    iter_count = 0
    while iter_count < max_iter:
        fa = func(a)
        fb = func(b)
        c = b - (fb * (b - a) / (fb - fa))
        fc = func(c)
        if abs(fc) < tol:
            return c, iter_count
        if fa * fc < 0:
            b = c
        else:
            a = c
        iter_count += 1
    return c, iter_count


# Testing functions
test_functions = [func1, func2, func3]
intervals = [(1, 2), (-5.5,-3.5), (-2,-1)]
initial_guesses = [(1.2,), (-4,), (-1.5,)]

results = []

for i, func in enumerate(test_functions):
    a, b = intervals[i]
    x0 = initial_guesses[i][0]

    bisection_root, bisection_iters = bisection_method(func, a, b)
    newton_root, newton_iters = newton_raphson_method(func, x0)
    secant_root, secant_iters = secant_method(func, a, b)
    regula_falsi_root, regula_falsi_iters = regula_falsi_method(func, a, b)

    results.append({
        'Function': f'Function {i + 1}',
        'Bisection': {'Root': bisection_root, 'Iterations': bisection_iters},
        'Newton-Raphson': {'Root': newton_root, 'Iterations': newton_iters},
        'Secant': {'Root': secant_root, 'Iterations': secant_iters},
        'Regula Falsi': {'Root': regula_falsi_root, 'Iterations': regula_falsi_iters}
    })

# Print results
for result in results:
    print(result['Function'])
    for method, res in result.items():
        if method != 'Function':
            print(f"{method}: Root = {res['Root']}, Iterations = {res['Iterations']}")
    print("\n")

# Ranking based on Number of Iterations
for result in results:
    methods = ['Bisection', 'Newton-Raphson', 'Secant', 'Regula Falsi']
    iterations = [result[method]['Iterations'] for method in methods]
    ranked_methods = sorted(zip(methods, iterations), key=lambda x: x[1])
    print(f"Ranking for {result['Function']} based on Number of Iterations:")
    for rank, (method, iters) in enumerate(ranked_methods, 1):
        print(f"{rank}. {method} - Iterations: {iters}")
    print("\n")


# Rate of Convergence (simplified heuristic)
def rate_of_convergence(method_name, iters):
    return 1 / iters


for result in results:
    methods = ['Bisection', 'Newton-Raphson', 'Secant', 'Regula Falsi']
    iterations = [result[method]['Iterations'] for method in methods]
    ranked_methods = sorted(zip(methods, iterations), key=lambda x: rate_of_convergence(*x), reverse=True)
    print(f"Ranking for {result['Function']} based on Rate of Convergence:")
    for rank, (method, iters) in enumerate(ranked_methods, 1):
        print(f"{rank}. {method} - Rate of Convergence: {rate_of_convergence(method, iters):.6f}")
    print("\n")
