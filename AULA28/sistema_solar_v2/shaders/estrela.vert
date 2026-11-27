#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in float aSize;

out vec3 corEstrela;

uniform mat4 view;
uniform mat4 projection;

void main()
{
    corEstrela = aColor;

    // Variável interna do GLSL que define o tamanho do ponto em pixels
    gl_PointSize = aSize;

    // Estrelas já estão no espaço do mundo (não precisam de matriz model)
    gl_Position = projection * view * vec4(aPos, 1.0);
}