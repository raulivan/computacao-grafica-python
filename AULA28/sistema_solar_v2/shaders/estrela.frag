#version 330 core

in vec3 corEstrela;
out vec4 FragColor;

void main()
{
    // gl_PointCoord vai de (0.0, 0.0) a (1.0, 1.0) dentro de cada ponto desenhado
    //  a distância do pixel atual até o centro (0.5, 0.5) para deixá-lo redondo
    float dist = length(gl_PointCoord - vec2(0.5));
    if (dist > 0.5) {
        discard; // Descarta os cantos do quadrado
    }

    // Cria um brilho suave (mais intenso no centro, apagando nas bordas)
    float brilho = 1.0 - smoothstep(0.1, 0.5, dist);
    FragColor = vec4(corEstrela * brilho, 1.0);
}