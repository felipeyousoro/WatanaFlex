Algoritmo tc10;
Variaveis
    inteiro: N,c;

Funcao Fat(N,c):inteiro;
    inteiro:N;
    inteiro:c;
inicio
    c <- c+1;
    se N>0 entao
        Fat <- Fat(N-1)*N;
    senao
        Fat <- 1;
    fim se;
fim;

Inicio
    N <- 3;
    c <- 0;
    {
        O proximo comando possui
        um erro lexico no parametro
        da chamada da funcao.
    }
    imprima(Fat(N,{erro lexico} #));
Fim.
