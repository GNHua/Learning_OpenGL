from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof

WIDTH = 800
HEIGHT = 600
GLfloat = c_float
GLuint = c_uint


class Window(QtGui.QOpenGLWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make sure to set the Surface Format in `__init__`.
        # Otherwise, it won't work.
        format = QtGui.QSurfaceFormat()
        format.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        format.setVersion(4, 1)
        self.setFormat(format)
        
        self.setTitle('LearnOpenGL')
        
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.)
        
        self.vertices = np.array([[ 0.5, -0.5, 0., 1., 0., 0.],
                                  [-0.5, -0.5, 0., 0., 1., 0.],
                                  [ 0. ,  0.5, 0., 0., 0., 1.]], dtype=GLfloat)
        self.indices = np.array([0, 1, 2], dtype=GLuint)
        
        ########################################################
        # Create a shader program
        
        self.shaderProg = QtGui.QOpenGLShaderProgram()
        self.shaderProg.create()
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, 'triangle.vert')
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, 'triangle.frag')
        self.shaderProg.link()
        ########################################################
        
        
        ########################################################
        # create a Vertex Array Object with vertice information
        
        self.VAO1 = QtGui.QOpenGLVertexArrayObject()
        self.VAO1.create()
        self.VAO1.bind()
        
        VBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
        VBO.create()
        VBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.vertices.tostring()
        VBO.bind()
        VBO.allocate(data, len(data))
        self.gl.glVertexAttribPointer(0, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 6*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        self.gl.glVertexAttribPointer(1, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 6*sizeof(GLfloat), 3*sizeof(GLfloat))
        self.gl.glEnableVertexAttribArray(1)
        
        EBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.IndexBuffer)
        EBO.create()
        EBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.indices.tostring()
        EBO.bind()
        EBO.allocate(data, len(data))
        
        VBO.release()
        self.VAO1.release()
        ########################################################
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        self.shaderProg.bind()
        self.VAO1.bind()
        self.gl.glDrawElements(self.gl.GL_TRIANGLES, 3,
            self.gl.GL_UNSIGNED_INT, None)
        self.VAO1.release()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        event.accept()


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())