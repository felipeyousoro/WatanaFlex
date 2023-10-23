#include <iostream>
#include <string>

#include "automata.c"

using namespace std;

class Automaton{
    private:
        int initial_state, current_index, token;
        string input, token_content;

        int get_next_token(){
            int last_final_state = 0, last_final_index = this->current_index, current_state = this->initial_state;

            for(int i = this->current_index; i < this->input.length(); i++){
                int next_state = TRANSITION_TABLE[current_state][input[i]];

                if(next_state != -1 && FINAL_STATES_TABLE[next_state] == true){
                    last_final_state = next_state;
                    last_final_index = i;
                }

                if(next_state == -1){
                    this->token_content = this->input.substr(this->current_index, i - this->current_index);
                    this->current_index = last_final_index + 1;
                    return STATE_TOKENS_TABLE[last_final_state];
                }

                current_state = next_state;
            }

            this->token_content = this->input.substr(this->current_index, this->input.length() - this->current_index);
            this->current_index = last_final_index + 1;
            return STATE_TOKENS_TABLE[last_final_state];
        }

    public:

    Automaton(int initial_state, string input){
        this->initial_state = initial_state;
        this->current_index = 0;
        this->input = input;
    }

    int advance(){
        if (this->current_index >= this->input.length()){
            cout << "Fim de arquivo" << endl;
            exit(0);
        }

        return this->get_next_token();
    }

};

int main(){
    string input; char symbol;
    while(cin.get(symbol)){
        input += symbol;
    }

    Automaton automaton(0, input);


    while(1) {
        int token = automaton.advance();
        if(token == ERRO){
            cout << "ERRO" << endl;
        } else if(token == VAZIO) {
            //cout << "VAZIO" << endl;
        } else if(token == ALGORITMO) {
            cout << "ALGORITMO" << endl;
        } else if(token == VETOR) {
            cout << "VETOR" << endl;
        } else if(token == ENQUANTO) {
            cout << "ENQUANTO" << endl;
        } else if(token == INICIO) {
            cout << "INICIO" << endl;
        } else if(token == MATRIZ) {
            cout << "MATRIZ" << endl;
        } else if(token == FACA) {
            cout << "FACA" << endl;
        } else if(token == VERDADEIRO) {
            cout << "VERDADEIRO" << endl;
        } else if(token == TIPO) {
            cout << "TIPO" << endl;
        } else if(token == PARA) {
            cout << "PARA" << endl;
        } else if(token == FALSO) {
            cout << "FALSO" << endl;
        } else if(token == VARIAVEIS) {
            cout << "VARIAVEIS" << endl;
        } else if(token == FUNCAO) {
            cout << "FUNCAO" << endl;
        } else if(token == DE) {
            cout << "DE" << endl;
        } else if(token == E) {
            cout << "E" << endl;
        } else if(token == INTEIRO) {
            cout << "INTEIRO" << endl;
        } else if(token == NUM_INTEIRO) {
            cout << "NUM_INTEIRO" << endl;
        } else if(token == PROCEDIMENTO) {
            cout << "PROCEDIMENTO" << endl;
        } else if(token == ATE) {
            cout << "ATE" << endl;
        } else if(token == OU) {
            cout << "OU" << endl;
        } else if(token == NUM_REAL) {
            cout << "NUM_REAL" << endl;
        } else if(token == SE) {
            cout << "SE" << endl;
        } else if(token == PASSO) {
            cout << "PASSO" << endl;
        } else if(token == NAO) {
            cout << "NAO" << endl;
        } else if(token == CARACTERE) {
            cout << "CARACTERE" << endl;
        } else if(token == ENTAO) {
            cout << "ENTAO" << endl;
        } else if(token == REPITA) {
            cout << "REPITA" << endl;
        } else if(token == DIV) {
            cout << "DIV" << endl;
        } else if(token == LOGICO) {
            cout << "LOGICO" << endl;
        } else if(token == SENAO) {
            cout << "SENAO" << endl;
        } else if(token == LEIA) {
            cout << "LEIA" << endl;
        } else if(token == PONTO_E_VIRGULA) {
            cout << "PONTO_E_VIRGULA" << endl;
        } else if(token == VIRGULA) {
            cout << "VIRGULA" << endl;
        } else if(token == DOIS_PONTOS) {
            cout << "DOIS_PONTOS" << endl;
        } else if(token == PONTO) {
            cout << "PONTO" << endl;
        } else if(token == ABRE_COLCHETES) {
            cout << "ABRE_COLCHETES" << endl;
        } else if(token == FECHA_COLCHETES) {
            cout << "FECHA_COLCHETES" << endl;
        } else if(token == ABRE_PARENTESES) {
            cout << "ABRE_PARENTESES" << endl;
        } else if(token == FECHA_PARENTESES) {
            cout << "FECHA_PARENTESES" << endl;
        } else if(token == IGUAL) {
            cout << "IGUAL" << endl;
        } else if(token == DIFERENTE) {
            cout << "DIFERENTE" << endl;
        } else if(token == MAIOR) {
            cout << "MAIOR" << endl;
        } else if(token == MAIOR_IGUAL) {
            cout << "MAIOR_IGUAL" << endl;
        } else if(token == MENOR) {
            cout << "MENOR" << endl;
        } else if(token == MENOR_IGUAL) {
            cout << "MENOR_IGUAL" << endl;
        } else if(token == IDENTIFICADOR) {
            cout << "IDENTIFICADOR" << endl;
        } else if(token == STRING) {
            cout << "STRING" << endl;
        } else if(token == COMENTARIO) {
            cout << "COMENTARIO" << endl;
        }
        else if(token == MAIS) {
            cout << "MAIS" << endl;
        }
        else if(token == MENOS) {
            cout << "MENOS" << endl;
        }
        else if(token == VEZES) {
            cout << "VEZES" << endl;
        }
        else if(token == DIVISAO) {
            cout << "DIVISAO" << endl;
        }
        else if(token == ATRIBUICAO) {
            cout << "ATRIBUICAO" << endl;
        }

    }


    return 0;
}