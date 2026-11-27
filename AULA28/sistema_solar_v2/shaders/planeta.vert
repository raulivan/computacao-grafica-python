#version 330 core

layout (location = 0) in vec3 aPos; // Posição do vértice
layout (location = 1) in vec3 aNormal; // Vetor normal da esfera
layout (location = 2) in vec2 aTexCoord; // Coordenada UV da textura (0.0 a 1.0)

out vec3 FragPos;
out vec3 Normal;
out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = mat3(transpose(inverse(model))) * aNormal;
    TexCoord = aTexCoord;

    gl_Position = projection * view * vec4(FragPos, 1.0);
}