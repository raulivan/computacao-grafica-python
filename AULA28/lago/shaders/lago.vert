#version 330 core

layout (location = 0) in vec3 aPos;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float tempo;

void main()
{
    vec3 pos = aPos;

    // Soma de 3 ondas senoidais/cossenoidais em direções distintas
    float w1 = 0.12 * sin(pos.x * 1.5 + tempo * 1.8);
    float w2 = 0.08 * cos(pos.z * 2.0 + tempo * 1.3);
    float w3 = 0.05 * sin((pos.x + pos.z) * 3.0 - tempo * 2.5);
    pos.y = w1 + w2 + w3;

    // Derivadas parciais para calcular a normal exata da onda
    float dydx = 0.12 * 1.5 * cos(pos.x * 1.5 + tempo * 1.8)
               + 0.05 * 3.0 * cos((pos.x + pos.z) * 3.0 - tempo * 2.5);

    float dydz = -0.08 * 2.0 * sin(pos.z * 2.0 + tempo * 1.3)
               + 0.05 * 3.0 * cos((pos.x + pos.z) * 3.0 - tempo * 2.5);

    vec3 normalLocal = normalize(vec3(-dydx, 1.0, -dydz));

    FragPos = vec3(model * vec4(pos, 1.0));
    Normal = mat3(transpose(inverse(model))) * normalLocal;

    gl_Position = projection * view * vec4(FragPos, 1.0);
}