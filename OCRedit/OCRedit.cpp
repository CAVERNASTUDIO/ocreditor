#include <iostream>
#include <cstdlib>
#include "ico.h" // Referencia al icono

int main() {
    int resultado = system("cmd /c call Scripts\\EJ.bat & pause");
    if (resultado == 0) {
        std::cout << "El archivo .bat se ejecutÃ³ correctamente." << std::endl;
    }
    else {
        std::cerr << "Hubo un error al ejecutar el archivo .bat." << std::endl;
    }
}


// Copyright (c) - 2026 Erik Alejandro García Aparcio - All rights reserved.
