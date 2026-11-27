#version 330 core

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

out vec4 FragColor;

// Tipo especial do GLSL que representa uma textura 2D na GPU
uniform sampler2D texturaPlaneta;
uniform bool ehSol; // Define se o astro emite luz própria
uniform vec3 lightPos; // Posição do Sol (0, 0, 0)
uniform vec3 viewPos; // Posição da câmera

void main()
{
    // Lê a cor do pixel correspondente na imagem da textura usando as coordenadas UV
    vec3 corTextura = texture(texturaPlaneta, TexCoord).rgb;

    // Se for o Sol, ignora sombras e exibe a textura com brilho máximo
    if (ehSol) {
        FragColor = vec4(corTextura, 1.0);
        return;
    }

    // ILUMINAÇÃO DE PHONG PARA OS PLANETAS
    vec3 corLuz = vec3(1.0, 0.98, 0.92); // Luz solar levemente quente

    // Ambiente (fraca, para o lado noturno do planeta ficar escuro, mas visível)
    vec3 ambient = 0.08 * corLuz;

    //Difusa (lado voltado para o Sol)
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * corLuz;

    //Especular (brilho sutil)
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16.0);
    vec3 specular = 0.15 * spec * corLuz;

    vec3 resultado = (ambient + diffuse + specular) * corTextura;
    FragColor = vec4(resultado, 1.0);
}