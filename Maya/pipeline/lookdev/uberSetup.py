"""
    uberSetup()

    __author__ = 'cargoyle'

    description: an attempt at creating an uber shader setup tool
        for the cgfx uberShader

"""
import pymel.core as pm

import pipeline.lookdev.devLighting as ld
import pipeline.lookdev.textureNode as tx

shdPath = str( pm.internalVar( uad = True ) + "scripts/pipeline/shaders/")

getSel = pm.ls(selection = True)

shdName = str(getSel[0]+"_CGFX")

cgfx = pm.shadingNode("cgfxShader", asShader = True, n = shdName)
pm.mel.eval('cgfxShader -e -fx  "'+shdPath+'cgfx/lcUberShader_3.0.cgfx" '+shdName+";")

# create file nodes for all textures and set them up
# setup diffuse
difNode = tx.texNode(cgfx, "Diffuse", getSel[0])
pm.setAttr(str(shdName+".useDiffuseMap"), True)
# now connect our new file node to the shader
difNode.outColor >> cgfx.diffuseMapSampler

# setup specular
specNode = tx.texNode(cgfx, "Specular", getSel[0])
pm.setAttr(str(shdName+".useSpecularMap"), True)
# now connect our new file node to the shader
specNode.outColor >> cgfx.specularMapSampler

# setup normal
nrmlNode = tx.texNode(cgfx, "Normal", getSel[0])
pm.setAttr(str(shdName+".useNormalMap"), True)
# now connect our new file node to the shader
nrmlNode.outColor >> cgfx.normalMapSampler


# I should check to see if this node exists before I just set it up
envNode = tx.texNode(cgfx, "Environment", "cgfx")
pm.setAttr("cgfxEnvironment_File.fileTextureName", str(shdPath+"shaders/CubeMaps/sunsetCube.dds"))
envNode.outColor >> cgfx.envCubeMapSampler

pm.setAttr(str(shdName+".useReflCube"), True)
pm.setAttr(str(shdName+".useAmbCube"), True)
# create a three point light setup
lights = ld.threePointlight("directional")
# connecting the lights to the shader
pm.mel.eval("cgfxShader_connectVector "+shdName+".light1Dir "+lights[0]+";")
pm.setAttr(str(shdName+".light1Color"),[1.0, 0.95, 0.82])
pm.mel.eval("cgfxShader_connectVector "+shdName+".light2Dir "+lights[1]+";")
pm.setAttr(str(shdName+".light2Color"),[0.61, 0.8, 1.0])
pm.mel.eval("cgfxShader_connectVector "+shdName+".light3Dir "+lights[2]+";")
pm.setAttr(str(shdName+".light3Color"),[0.4, 0.4, 0.4])

# assign Material
# create a surface Shader and attach out cgfx shader to it.
cgfxShd = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=str(shdName+"SurfaceShader"))
cgfx.outColor >> cgfxShd.surfaceShader
# Assign the Shader to the objects
pm.sets(cgfxShd, edit=True, forceElement=getSel[0])