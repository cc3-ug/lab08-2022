#include "sum.h"

static __inline__ uint64_t now() {
  struct timespec now;
  clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &now);
  return now.tv_nsec;
}


static int sum_naive(int n, int *a) {
  int sum = 0;
  for (int i = 0; i < n; i++) {
    sum += a[i];
  }
  return sum;
}


static int sum_unrolled(int n, int *a) {
  int sum = 0;

  // unrolled loop
  for (int i = 0; i < n / 4 * 4; i += 4) {
    sum += a[i+0];
    sum += a[i+1];
    sum += a[i+2];
    sum += a[i+3];
  }

    // tail case
  for (int i = n / 4 * 4; i < n; i++) {
    sum += a[i];
  }

  return sum;
}


static int sum_vectorized(int n, int *a) {

  /*
    Inicializar un registro de SIMD con ceros

    Ciclo principal
      A los registros SIMD les caben cuatro int
      Obtenemos datos de memoria
      Sumamos
    Al terminar el ciclo, casi todo el arreglo se sumo
    
    Pasamos esos resultados parciales a un arreglo normal

    Tenemos cuatro resultados parciales, los sumamos

    Tail case
      Si la cantidad de casillas del arreglo no es divisible dentro de 4, faltan casillas por sumar
      Accedemos al arreglo de forma normal, ya sin SIMD
      Sumamos
    
    Listo!
  */

  return 0;
}


static int sum_vectorized_unrolled(int n, int *a) {
  
  /*
    Inicializar un registro de SIMD con ceros

    Ciclo principal
      A los registros SIMD les caben cuatro int
      Quiero hacer unroll de 4
      Entonces...
      
      Obtenemos datos de memoria
      Sumamos
      Obtenemos datos de memoria
      Sumamos
      Obtenemos datos de memoria
      Sumamos
      Obtenemos datos de memoria
      Sumamos
    Al terminar el ciclo, casi todo el arreglo se sumo
    
    Pasamos esos resultados parciales a un arreglo normal

    Tenemos cuatro resultados parciales, los sumamos

    Tail case
      Dependiendo de la cantidad de casillas del arreglo, quizas falten casillas por sumar
      Accedemos al arreglo de forma normal, ya sin SIMD
      Sumamos
    
    Listo!
  */
  
  return 0;
}


void benchmark(int n, int *a, int(*computeSum)(int, int*), char *name) {
  // warm up cache
  int sum = computeSum(n, a);

  // measure
  uint64_t start = now();
  sum += computeSum(n, a);
  uint64_t time = now() - start;
  double microseconds = time / 1e3;

  // print results
  printf("%20s: ", name);
  if (sum == 2 * sum_naive(n, a))
    printf("%.2f microseconds\n", microseconds);
  else
    printf("ERROR! la suma con SIMD no coincide con el resultado base\n");
}


int main(int argc, char **argv){
  const int n = 7777;

  // initialize the array with random values
  srand48(time(NULL));
  int a[n] __attribute__((aligned(16)));
  for (int i = 0; i < n; i++){
    a[i] = lrand48();
  }

  // benchmark series of codes
  benchmark(n, a, sum_naive, "naive");
  benchmark(n, a, sum_unrolled, "unrolled");
  benchmark(n, a, sum_vectorized, "vectorized");
  benchmark(n, a, sum_vectorized_unrolled, "vectorized unrolled");

  return 0;
}
