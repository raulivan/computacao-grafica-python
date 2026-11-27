#version 330 core

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

uniform vec3 viewPos;
uniform vec3 sunDir;

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    // Cor base da água profunda
    vec3 corAguaFunda = vec3(0.01, 0.15, 0.25);

    // Reflexo procedural do céu baseado no ângulo de reflexão
    vec3 reflectDir = reflect(-viewDir, norm);
    float fatorCeu = clamp(reflectDir.y, 0.0, 1.0);
    vec3 corHorizonte = vec3(0.65, 0.80, 0.92);
    vec3 corTopoCeu   = vec3(0.15, 0.45, 0.85);
    vec3 corReflexoCeu = mix(corHorizonte, corTopoCeu, pow(fatorCeu, 0.6));

    // Efeito Fresnel (Aproximação de Schlick)
    float fresnel = 0.04 + 0.96 * pow(1.0 - max(dot(norm, viewDir), 0.0), 4.0);
    vec3 corFinal = mix(corAguaFunda, corReflexoCeu, fresnel);

    // Brilho especular do Sol nas cristas das ondas
    float spec = pow(max(dot(reflectDir, normalize(sunDir)), 0.0), 180.0);
    vec3 corSol = vec3(1.0, 0.95, 0.85);
    corFinal += corSol * spec * 1.5;

    FragColor = vec4(corFinal, 1.0);
}