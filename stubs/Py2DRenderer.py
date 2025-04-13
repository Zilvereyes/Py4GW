from typing import List
import PyOverlay 



class Py2DRenderer:
    def __init__(self) -> None: ...

    def set_primitives(self, shapes: List[List[PyOverlay.Point2D]], color: int) -> None: ...
    def set_world_zoom_x(self, zoom: float) -> None: ...
    def set_world_zoom_y(self, zoom: float) -> None: ...
    def set_world_pan(self, x:float, y:float) -> None: ...
    def set_world_rotation(self, rotation: float) -> None: ...
    def set_world_space(self, enabled: bool) -> None: ...
    
    def set_screen_offset(self, x: float, y: float) -> None: ...
    def set_screen_zoom_x(self, zoom: float) -> None: ...
    def set_screen_zoom_y(self, zoom: float) -> None: ...
    def set_screen_rotation(self, rotation: float) -> None: ...

    def set_circular_mask(self, enabled: bool) -> None: ...
    def set_mask_radius(self, radius: float) -> None: ...
    def set_mask_center(self, x: float, y: float) -> None: ...
    
    def set_rectangle_mask(self, enabled: bool) -> None: ...
    def set_rectangle_mask_bounds(self, x: float, y: float, width: float, height: float) -> None: ...

    def render(self) -> None: ...

    def Setup3DView(self) -> None: ...
    def DrawLine(self,_from: PyOverlay.Point2D , _to: PyOverlay.Point2D, color:int, thickness:float) -> None: ...
    def DrawTriangle(self, p1: PyOverlay.Point2D, p2: PyOverlay.Point2D, p3: PyOverlay.Point2D, color:int, thickness:float) -> None: ...
    def DrawTriangleFilled(self, p1: PyOverlay.Point2D, p2: PyOverlay.Point2D, p3: PyOverlay.Point2D, color:int) -> None: ...
    def DrawQuad(self, p1: PyOverlay.Point2D, p2: PyOverlay.Point2D, p3: PyOverlay.Point2D, p4: PyOverlay.Point2D, color:int, thickness:float) -> None: ...
    def DrawQuadFilled(self, p1: PyOverlay.Point2D, p2: PyOverlay.Point2D, p3: PyOverlay.Point2D, p4: PyOverlay.Point2D, color:int) -> None: ...
    def DrawPoly(self, center: PyOverlay.Point2D, radius:float , color:int, segments:int, thickness:float) -> None: ...
    def DrawPolyFilled(self, center: PyOverlay.Point2D, radius:float , color:int, segments:int) -> None: ...
    
    def DrawLine3D(self, _from: PyOverlay.Point3D, _to: PyOverlay.Point3D, color:int, use_occlusion:bool) -> None: ...
    def DrawTriangle3D(self, p1: PyOverlay.Point3D, p2: PyOverlay.Point3D, p3: PyOverlay.Point3D, color:int, use_occlusion:bool) -> None: ...
    def DrawTriangleFilled3D(self, p1: PyOverlay.Point3D, p2: PyOverlay.Point3D, p3: PyOverlay.Point3D, color:int, use_occlusion:bool) -> None: ...
    def DrawQuad3D(self, p1: PyOverlay.Point3D, p2: PyOverlay.Point3D, p3: PyOverlay.Point3D, p4: PyOverlay.Point3D, color:int, use_occlusion:bool) -> None: ...
    def DrawQuadFilled3D(self, p1: PyOverlay.Point3D, p2: PyOverlay.Point3D, p3: PyOverlay.Point3D, p4: PyOverlay.Point3D, color:int, use_occlusion:bool) -> None: ...
    def DrawPoly3D(self, center: PyOverlay.Point3D, radius:float , color:int, segments:int, use_occlusion:bool) -> None: ...
    def DrawPolyFilled3D(self, center: PyOverlay.Point3D, radius:float , color:int, segments:int, use_occlusion:bool) -> None: ...
    def DrawCubeOutline(self, center: PyOverlay.Point3D, size:float , color:int, use_occlusion:bool) -> None: ...
    def DrawCubeFilled(self, center: PyOverlay.Point3D, size:float , color:int, use_occlusion:bool) -> None: ...