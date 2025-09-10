@echo off
setlocal

:: Create checkpoints directory
if not exist "checkpoints" (
    mkdir checkpoints
)

:: Download files using curl if they don't exist
echo Downloading SadTalker model files...

:: New release (OpenTalker)
if not exist "checkpoints\mapping_00109-model.pth.tar" (
    curl -L -o checkpoints\mapping_00109-model.pth.tar https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar
)

if not exist "checkpoints\mapping_00229-model.pth.tar" (
    curl -L -o checkpoints\mapping_00229-model.pth.tar https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar
)

if not exist "checkpoints\SadTalker_V0.0.2_256.safetensors" (
    curl -L -o checkpoints\SadTalker_V0.0.2_256.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors
)

if not exist "checkpoints\SadTalker_V0.0.2_512.safetensors" (
    curl -L -o checkpoints\SadTalker_V0.0.2_512.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors
)

:: Optional (Uncomment if using BFM_Fitting and hub)
REM curl -L -o checkpoints\BFM_Fitting.zip https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/BFM_Fitting.zip
REM powershell -Command "Expand-Archive -Path 'checkpoints\BFM_Fitting.zip' -DestinationPath 'checkpoints' -Force"

REM curl -L -o checkpoints\hub.zip https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/hub.zip
REM powershell -Command "Expand-Archive -Path 'checkpoints\hub.zip' -DestinationPath 'checkpoints' -Force"

:: Create enhancer weights folder
if not exist "gfpgan\weights" (
    mkdir gfpgan\weights
)

:: Download enhancer model files
echo Downloading enhancer (GFPGAN) weights...

if not exist "gfpgan\weights\alignment_WFLW_4HG.pth" (
    curl -L -o gfpgan\weights\alignment_WFLW_4HG.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth
)

if not exist "gfpgan\weights\detection_Resnet50_Final.pth" (
    curl -L -o gfpgan\weights\detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
)

if not exist "gfpgan\weights\GFPGANv1.4.pth" (
    curl -L -o gfpgan\weights\GFPGANv1.4.pth https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
)

if not exist "gfpgan\weights\parsing_parsenet.pth" (
    curl -L -o gfpgan\weights\parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth
)

echo All files downloaded successfully.
pause
