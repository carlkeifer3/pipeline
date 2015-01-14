"""
    textureNode.py
    __author__ = 'cargoyle'

    description = creates a new texture and 2d uv placement node

"""

def texNode(cgfx, texType, shdName):
    """

    :return:
    """
    import pymel.core as pm

    # create file nodes for all textures and set them up
    texFile = pm.shadingNode("file", asTexture = True, n = str(shdName+texType+"_File"))
    placeUV = pm.shadingNode("place2dTexture", asUtility = True, n = str(shdName+texType+"_uvPlace"))
    placeUV.coverage >> texFile.coverage
    placeUV.translateFrame >> texFile.translateFrame
    placeUV.rotateFrame >> texFile.rotateFrame
    placeUV.mirrorU >> texFile.mirrorU
    placeUV.mirrorV >> texFile.mirrorV
    placeUV.stagger >> texFile.stagger
    placeUV.wrapU >> texFile.wrapU
    placeUV.wrapV >> texFile.wrapV
    placeUV.repeatUV >> texFile.repeatUV
    placeUV.offset >> texFile.offset
    placeUV.rotateUV >> texFile.rotateUV
    placeUV.noiseUV >> texFile.noiseUV
    placeUV.vertexUvOne >> texFile.vertexUvOne
    placeUV.vertexUvTwo >> texFile.vertexUvTwo
    placeUV.vertexUvThree >> texFile.vertexUvThree
    placeUV.vertexCameraOne >> texFile.vertexCameraOne
    placeUV.outUV >> texFile.uv
    placeUV.outUvFilterSize >> texFile.uvFilterSize

    return texFile