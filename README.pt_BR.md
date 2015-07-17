# Clover
Clover é um anti-malware super simples para Windows que visa impedir infecções de malwares em tempo de execução. 

Desenvolvido para ser simples. Melhor utilizado quando aliado ao bom-senso.

## Funcionalidades
* Monitoramento das chaves de inicialização do Windows
* Ferramentas forenses falsas, utilizando de arquivos iscas para detectar técnicas de anti-debugging

## Funcionalidades que não serão implementadas
Algumas funcionalidades não serão implementadas no Clover, por serem contra a filosofia da simplicidade:
* Auto updates
* Signature-based detection

## Download
### Instalador
[Clover 1.0](https://github.com/clover-av/clover/blob/master/bin/Clover_Antimalware_1_0_Setup.exe?raw=true)

Ao instalar esse software, você concorda com sua licença GNU General Public License 3. Você pode ler ela [aqui](https://github.com/clover-av/clover/blob/master/LICENSE.md). 

## Requisitos minímos
Os requisitos são mínimos, de verdade. 
- Windows XP, 7, 8
- 12MB de RAM
- 30MB de espaço livre no HD

## Como compilar?
Para compilar, você precisará do [PyInstaller](https://github.com/pyinstaller/pyinstaller/wiki) e do (Python 2.7)[https://www.python.org/download/releases/2.7] instalados.

Acesse o diretório *src* do Clover e execute:

    pyinstaller.exe --icon clover.ico --noconsole

Para compilar os arquivos baits, você precisará do compilador g++.

    g++.exe wireshark.exe
