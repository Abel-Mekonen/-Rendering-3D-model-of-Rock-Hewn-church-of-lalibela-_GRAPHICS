
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import os
import numpy as np
from PIL import Image
import glm as glm
from obj_loader import Loader





class glapp:

    def __init__(self):

        pygame.init()
        pygame.display.set_mode((1024 , 612),DOUBLEBUF|OPENGL)
        glClearColor(0,0,0,1.0)
        pygame.mouse.set_pos(612,306)
      
        glViewport(0,0,1024,612)

        self.yaw = -90
        self.pitch = 0

       
        self.vertexShader = self.getFileContents("triangle.vertex.shader")
        self.fragmentShader = self.getFileContents("triangle.fragment.shader")
        self.vertexShaderComp = compileShader(self.vertexShader , GL_VERTEX_SHADER)
        self.fragmentShaderComp = compileShader(self.fragmentShader , GL_FRAGMENT_SHADER)
        self.program = glCreateProgram()

        self.view =  glm.mat4(1.0)
        self.projection = glm.mat4(1.0)

        self.model1 = glm.mat4(1.0)
        self.model2 = glm.mat4(1.0)
        self.model3 = glm.mat4(1.0)
        self.model4 = glm.mat4(1.0)

        model1 = glm.rotate(self.model1 , glm.radians(45) , glm.vec3(0, 1 , 0))
        model2 = glm.rotate(self.model2 , glm.radians(45) , glm.vec3(0, 1 , 0))
        model3 = glm.rotate(self.model3 , glm.radians(45) , glm.vec3(0, 1 , 0))
        model4 = glm.rotate(self.model4 , glm.radians(45) , glm.vec3(0, 1 , 0))
        self.model = [model1 , model2 , model3 , model4]

        self.view = glm.translate(self.view , glm.vec3(0 , 0 , 0))
        self.projection = glm.perspective(glm.radians(45) , 1024/612 , 0.1 , 400)

        self.cameraPos = glm.vec3(0,30,60)
        self.cameraFront = glm.vec3(0 , 0 ,-3)
        self.cameraUp = glm.vec3(0 , 1 , 0)

        glAttachShader(self.program , self.vertexShaderComp)
        glAttachShader(self.program , self.fragmentShaderComp)
        glLinkProgram(self.program)

        loader = Loader("obj file/ground.obj")
        loader2 = Loader("obj file/lalibela area.obj")
        loader3 = Loader("obj file/lalibela green.obj")
        # loader4 = Loader("obj file/lalibela green2.obj")

        vertices = np.array(loader.verticeFinal , dtype= np.float32)
        vertices2 = np.array(loader2.verticeFinal , dtype= np.float32)
        vertices3 = np.array(loader3.verticeFinal , dtype= np.float32)
        # vertices4 = np.array(loader4.verticeFinal , dtype= np.float32)

        self.vertices = [vertices , vertices2 , vertices3 ]

        self.VAO = glGenVertexArrays(3)
        self.VBO = glGenBuffers(3)

        # Generate texture buffers and binding the buffer
        self.texture = glGenTextures(4)
        self.bindBuffer("images/grouned_baked.png" , 0)
        self.bindBuffer("images/abel_lalibela_baked.png" , 1)
        self.bindBuffer("images/green.jpg" , 2)
       
        
        glBindVertexArray(0)
        self.main()





    def bindBuffer(self , imageName , index):

        glBindVertexArray(self.VAO[index])
        glBindBuffer(GL_ARRAY_BUFFER , self.VBO[index])
        glBufferData(GL_ARRAY_BUFFER , self.vertices[index].nbytes , self.vertices[index] , GL_STATIC_DRAW)

        position = glGetAttribLocation(self.program , "position")
        glVertexAttribPointer(0 , 3 , GL_FLOAT , GL_FALSE , self.vertices[index].itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        textureloc = glGetAttribLocation(self.program, "texCoord");
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*self.vertices[index].itemsize, ctypes.c_void_p(12))
        glEnableVertexAttribArray(textureloc)

        glBindTexture(GL_TEXTURE_2D, self.texture[index])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open(imageName)
        width, height = image.size

        image_data = image.convert("RGBA").tobytes()
      
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,GL_UNSIGNED_BYTE, image_data)

        glGenerateMipmap(GL_TEXTURE_2D)



    def getFileContents(self,filename):
        p = os.path.join(os.getcwd(), "shaders3", filename)
        return open(p, 'r').read()

    def drawer(self,index):


        glBindVertexArray(self.VAO[index])
        glBindTexture(GL_TEXTURE_2D , self.texture[index])
        location1 = glGetUniformLocation(self.program , "model")
        glUniformMatrix4fv(location1 , 1 , GL_FALSE , glm.value_ptr(self.model[index]))
        location = glGetUniformLocation(self.program , "view")
        glUniformMatrix4fv(location , 1 , GL_FALSE , glm.value_ptr(self.view))
        location3 = glGetUniformLocation(self.program , "projection")
        glUniformMatrix4fv(location3 , 1 , GL_FALSE , glm.value_ptr(self.projection))
        glDrawArrays(GL_TRIANGLES , 0 , len(self.vertices[index]))



    def mouseMotion(self , position):

        self.yaw -=( position[0] * 0.5)
        self.pitch -= (position[1] * 0.5)


        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89):
            self.pitch = -89

        x = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))  
        y = np.sin(np.radians(self.pitch)) 
        z = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))

        front = glm.vec3(x,y,z)
        self.cameraFront = glm.normalize(front) 
       


    def keyBoardMotion(self , event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        if event.key == pygame.K_DOWN:
            self.cameraPos -= 2 * self.cameraFront
        if event.key == pygame.K_UP:
            self.cameraPos +=  2 * self.cameraFront
        if event.key == pygame.K_RIGHT:
            self.cameraPos += glm.normalize(glm.cross(self.cameraFront , self.cameraUp)) 
        if event.key == pygame.K_LEFT:
            self.cameraPos -= glm.normalize(glm.cross(self.cameraFront , self.cameraUp)) 


    def main(self):
        print(len(self.texture))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.keyBoardMotion(event)
                    

            self.mouseMotion(pygame.mouse.get_rel())
            self.view = glm.lookAt(self.cameraPos , self.cameraPos + self.cameraFront , self.cameraUp)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.program)
            for i in range(len(self.VAO)):
                self.drawer(i)
            
            
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    app = glapp()
   