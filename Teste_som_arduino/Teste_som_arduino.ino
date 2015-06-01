#include "pitches.h"
#define NO_SOUND 0

// Notas que devem ser tocadas ordenadamente;
// arrays de cada compasso da musica

int melodia[] = {
 NOTE_D3, NO_SOUND, NOTE_F3, NO_SOUND, NOTE_G3, NO_SOUND, NOTE_D3,
 NO_SOUND, NOTE_F3, NO_SOUND, NOTE_GS3, NOTE_G3, NO_SOUND,
 NOTE_D3, NO_SOUND, NOTE_F3, NO_SOUND, NOTE_G3, NO_SOUND, NOTE_F3,
 NO_SOUND, NOTE_D3, NO_SOUND, NO_SOUND
}


 ;
// Duração das Notas: Colcheia:8; Semínima: 4; Mínima:2; Semibreve:1
int tempoNotas[] ={
   8,8,8,8,4,8,8,
   8,8,8,8,4,4,
   8,8,8,8,4,8,8,
   8,8,4,4
};
const int compasso = 2300; // Altera o compasso da música
void setup(){
  
 // int melodia[] = compasso
  
  for (int Nota = 0; Nota <sizeof(melodia)-1; Nota++){//o número 7 indica quantas notas tem a nossa matriz.
    int tempo = compasso/tempoNotas[Nota]; //Tempo = compasso dividido pela indicação da matriz tempoNotas.
    tone(11, melodia[Nota],tempo); //Toca a nota indicada pela matriz melodia durante o tempo.
    // Para distinguir as notas adicionamos um tempo entre elas (tempo da nota + 20%).
    delay(tempo*1.2);
  }
}
void loop(){
  //Não é necessária a repetição pois a mesma será feita pelo botão Reset.
}
//Fim de Programa
