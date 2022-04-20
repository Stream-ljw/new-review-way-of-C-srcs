
import sys,math

from PyQt5.QtWidgets import QApplication, QGraphicsScene , QGraphicsView, \
                            QGraphicsPathItem
from PyQt5.QtCore import  Qt,QPointF
from PyQt5.QtGui import QPainterPath, QPolygonF ,QPainter


class draw_arrow(QGraphicsPathItem):
    
    def __init__(self,source: QPointF = None, dest: QPointF =None):
        super().__init__()
        self._sourceItem = source
        self._destItem = dest
        
        self._arrow_height = 5
        self._arrow_width = 4
    
    def setSource(self, point: QPointF):
        self._sourceItem = point
    
    def setDest(self, point: QPointF):
        self._destItem = point

    def draw_directlinePath(self):
        path = QPainterPath(self._sourceItem)
        path.lineTo(self._destItem)
        return path
    
    def arrowPosCalc(self, start_point = None, end_point = None):
        try:
            startPoint, endPoint = start_point, end_point

            if startPoint is None:
                startPoint = self._sourceItem

            if endPoint is None:
                endPoint = self._destItem

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize

            # perpendicular vector
            perpX = -normY
            perpY = normX

            leftX = endPoint.x() + self._arrow_height * normX + self._arrow_width * perpX
            leftY = endPoint.y() + self._arrow_height * normY + self._arrow_width * perpY
            #print('stream@@@@  = {} : {} '.format(rightX ,rightY))
            rightX = endPoint.x() + self._arrow_height * normX - self._arrow_height * perpX
            rightY = endPoint.y() + self._arrow_height * normY - self._arrow_width * perpY
            #print('stream@@@@  = {} : {} '.format(rightX ,rightY))
            point2 = QPointF(leftX, leftY)
            point3 = QPointF(rightX, rightY)

            return QPolygonF([point2, endPoint, point3])

        except (ZeroDivisionError, Exception):
            return None


    def paint(self, painter: QPainter, option, widget=None) -> None:

        painter.setRenderHint(painter.Antialiasing)

        painter.pen().setWidth(2)
        painter.setBrush(Qt.NoBrush)

        path = self.draw_directlinePath()
        painter.drawPath(path)
        self.setPath(path)

        # change path.PointAtPercent() value to move arrow on the line
        triangle_source = self.arrowPosCalc(path.pointAtPercent(0.1), self._sourceItem)

        if triangle_source is not None:
            painter.drawPolyline(triangle_source)



class GraphicsView_field(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.resize(300,300)
        # 设置场景坐标原点和大小
        self.back_scene = QGraphicsScene()
        self.path = draw_arrow(QPointF(150.0,80.0),QPointF(150.0,60.0))
        
        self.back_scene.addItem(self.path)
        self.setScene(self.back_scene)

        #print('stream echo : {0}, {1}'.format(self.rect_item1.scenePos().x(), self.rect_item1.scenePos().y()))
        #print('stream echo : {0}, {1}'.format(self.rect_item2.scenePos().x(), self.rect_item2.scenePos().y()))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = GraphicsView_field()

    demo.show()

    sys.exit(app.exec_())




#  有一个类是专门 绘制图形 并且将内容填充进去

# 还有一个类是专门将上面绘制好的图形 通过 箭头连接起来 并进行显示


