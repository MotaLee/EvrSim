import wx,interval,copy
import numpy as np
from core import esui
yu=esui.YU
Itv=interval.Interval
# Panel container wx sub class;
class DivBase(object):
    ''' Styled Div Base. Call __init__ after wx control initilization.'''
    def __init__(self,parent:wx.Window,**argkw):
        self._flag_hover=False
        self._flag_active=False
        self._flag_passing=argkw.get('passing',False)
        self._bgi=None

        self.parent=parent
        self.label=argkw.get('label','')
        self.style=copy.deepcopy({'p':(0,0),'s':(0,0),'bgc':esui.COLOR_BACK})
        self.style_active=dict()
        self.style_hover=dict()
        self.updateStyle(**argkw)

        self.cn=argkw.get('cn','')
        self.SetName(self.cn)
        if 'tip' in argkw:self.SetToolTip(argkw['tip'])

        self.Bind(wx.EVT_LEFT_DOWN,self._onClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self._onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self._onLeave)
        self.Bind(wx.EVT_PAINT,self._onPaint)
        if self.style['bgc']!='TRANSPARENT':
            self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Refresh()
        return

    def _onPaint(self,e):
        if self.style['bgc']!='TRANSPARENT':
            dc=wx.BufferedPaintDC(self)
        else:
            dc=wx.PaintDC(self)
        _style=copy.deepcopy(self.style)
        if self._flag_hover:
            _style.update(self.style_hover)
        if self._flag_active:
            _style.update(self.style_active)

        if _style['bgc']=='TRANSPARENT':
            pen=wx.TRANSPARENT_PEN
            brush=wx.TRANSPARENT_BRUSH
        else:
            pen=wx.Pen(_style['bgc'])
            brush=wx.Brush(_style['bgc'])
        dc.SetPen(pen)
        dc.SetBrush(brush)
        dc.DrawRectangle((0,0),self.Size)
        if 'bgi' in _style:
            dc.DrawBitmap(self._bgi,0,0)

        border_width_all=_style.get('border_width',1)
        if 'border_up' in _style:
            bw=_style.get('border_up_width',border_width_all)
            dc.SetPen(wx.Pen(_style['border_up'],width=bw))
            dc.DrawLine(0,1,self.Size.x,1)
        if 'border_bottom' in _style:
            bw=_style.get('border_bottom_width',border_width_all)
            dc.SetPen(wx.Pen(_style['border_bottom'],width=bw))
            dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        if 'border_left' in _style:
            bw=_style.get('border_left_width',border_width_all)
            dc.SetPen(wx.Pen(_style['border_left'],width=bw))
            dc.DrawLine(1,0,1,_style.y)
        if 'border_right' in _style:
            bw=_style.get('border_right_width',border_width_all)
            dc.SetPen(wx.Pen(_style['border_right'],width=bw))
            dc.DrawLine(self.Size.x-1,0,self.Size.x-1,self.Size.y)

        if _style.get('border',''):
            dc.SetPen(wx.Pen(_style['border'],
                width=border_width_all))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle((0,0),self.Size)
        if self.label!='':
            tsize=_style.get('text_size',yu)
            dc.SetFont(esui.ESFont(size=tsize))
            tclr=_style.get('text',esui.COLOR_TEXT)
            dc.SetTextForeground(tclr)
            # dc.SetTextBackground(self.style.get('text',esui.COLOR_TEXT))
            align=_style.get('align','center')
            pad=_style.get('padding',0)
            tsize=dc.GetTextExtent(self.label)
            if align=='left':x=pad
            elif align=='center':x=(self.Size.x-tsize.x)/2
            else:x=self.Size.x-pad-tsize.x
            dc.DrawText(self.label,x,(self.Size.y-tsize.y)/2)
        return

    def updateStyle(self,**argkw):
        ''' Update style.
            * Argkw: style/hover/active;'''
        if 'style' in argkw:
            self.style.update(argkw.get('style'))
        if 'active' in argkw:
            self.style_active.update(argkw.get('active'))
        if 'hover' in argkw:
            self.style_hover.update(argkw.get('hover'))

        self.SetSize(self.style['s'])
        self.SetPosition(self.style['p'])
        self.BackgroundColour=self.style['bgc']
        if 'bgi' in self.style:
            self._bgi=esui.UMR.getImg(
                path=self.style['bgi'],
                w=self.Size[0],
                h=self.Size[1])

        if self.style['bgc']!='TRANSPARENT':
            self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Refresh()
        return

    def _onClk(self,e:wx.Event):
        e.Skip()
        self.setActive()
        if self._flag_passing:
            self.parent.ProcessEvent(e)
        return

    def _onEnter(self,e:wx.Event):
        e.Skip()
        self._flag_hover=True
        self.Refresh()
        return

    def _onLeave(self,e:wx.Event):
        e.Skip()
        self._flag_hover=False
        self.Refresh()
        return

    def setActive(self,active=None)->bool:
        if active is None:
            self._flag_active=not self._flag_active
        else:
            self._flag_active=active
        self.Refresh()
        return self._flag_active

    def isActive(self):
        return self._flag_active

    def getChildren(self):
        return self.Children

    def delChildren(self):
        self.DestroyChildren()
        return

    def setLabel(self,label):
        ' Set label and refresh.'
        self.label=str(label)
        self.Refresh()
        return
    pass

class Div(DivBase,wx.Panel):
    ''' Styled div control.'''
    def __init__(self,parent:wx.Window,**argkw):
        ''' Para argkw including:
            * label: a text showing in control;
            * tip: Tool tip text;
            * cn: Control name string. Link to wx Name attr;
            * passing: If pass event to parent, False default;
            * style: A dict allowed following keys:
                    * `p`: position, zreos default. `(int,int)`;
                    * `s`: size, zreos default. `(int,int)`;
                    * `bgc`: background color, COLOR_LBACK default. Or TRANSPARENT;
                    * `fgc`: foreground color, COLOR_FRONT default;
                    * `bgi`: background image path;
                    * `border`: all border color;
                    * `border_width`: all border width;
                    * `border_dir`: one side border color, dir for up/bottom/left/right;
                    * `border_dir_width`: one side border width;
                    * `text`: text color;
                    * `text_size`: text size, yu default;
                    * `padding`: text padding. 0 default;
                    * `align`: text align. Enum for `center`/left/right;
                * active: A style dict applied when active;
            * hover: A style dict applied when mouse on;'''
        wx.Panel.__init__(self,parent,style=wx.NO_BORDER)
        DivBase.__init__(self,parent,**argkw)
        return

    pass

class ScrollDiv(DivBase,wx.ScrolledWindow):
    def __init__(self, parent: wx.Window, **argkw):
        ''' Scrollable div.
            * `axis` : 'Y' default for vertical scroll, 'X' for horizontal;
            * `bar` : if display scroll bar,False default;'''
        wx.ScrolledWindow.__init__(self,parent)
        DivBase.__init__(self,parent, **argkw)
        self.rx=0   # Current x;
        self.ry=0   # Current y;
        self.mx=self.Size[0]    # Max width;
        self.my=self.Size[1]    # Max height;
        self.axis=argkw.get('axis','Y')
        self._flag_bar=argkw.get('bar',False)
        self.div_bar=Div(self,style={
            'p':(self.Size[0]-0.75*yu,yu),
            's':(yu/2,self.Size[1]-2*yu),
            'bgc':esui.COLOR_FRONT})
        self._list_block=[self.div_bar]
        if self.axis=='Y':self.SetExtraStyle(wx.VSCROLL)
        else:self.SetExtraStyle(wx.HSCROLL)
        if not self._flag_bar:self.div_bar.Hide()
        # self.SetScrollbar()
        self.SetScrollRate(1,1)
        self.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotWhl)
        self.Bind(wx.EVT_LEAVE_WINDOW,self._onLeave)
        return

    def scroll(self,dx,dy):
        dx=int(dx*yu)
        dy=int(dy*yu)
        self.rx+=dx
        self.ry+=dy
        # for ctrl in self.Children:
            # ctrl.SetPosition((ctrl.Position[0]-dx,ctrl.Position[1]-dy))
        self.Scroll(self.rx,self.ry)
        return

    def updateMaxSize(self):
        xlist=[self.Size[0]]
        ylist=[self.Size[1]]
        for ctrl in self.Children:
            if ctrl.Shown and ctrl not in self._list_block:
                xlist.append(ctrl.Position[0]+ctrl.Size[0])
                ylist.append(ctrl.Position[1]+ctrl.Size[1])
        self.mx=max(xlist)
        self.my=max(ylist)
        if self.axis=='X':
            self.div_bar.SetSize(self.Size[1]**2/self.mx,yu/2)
        else:
            self.div_bar.SetSize(yu/2,self.Size[1]**2/self.my)
        self.SetVirtualSize(self.mx,self.my)
        self.Refresh()
        return

    def onRotWhl(self,e):
        t=-1*np.sign(e.WheelRotation)
        if self.axis=='X':
            if self.rx+t*yu not in Itv(0,self.mx-self.Size[0]):return
            self.scroll(t,0)
            self.div_bar.SetPosition((
                self.Size[1]-0.75*yu,
                self.rx*(self.Size[0]/self.mx)))
        elif self.axis=='Y':
            if self.ry+t*yu not in Itv(0,self.my-self.Size[1]):return
            self.scroll(0,t)
            self.div_bar.SetPosition((
                self.Size[0]-0.75*yu,
                self.ry*(self.Size[1]/self.my)))
        self.div_bar.Show()
        for ctrl in self.Children:
            ctrl.Refresh()
        return

    def getChildren(self):
        children=[ctrl for ctrl in self.Children if ctrl not in self._list_block]
        return children

    def delChildren(self):
        for ctrl in self.Children:
            if ctrl not in self._list_block:
                ctrl.Destroy()
        return

    def _onLeave(self,e:wx.Event):
        if not self._flag_bar:self.div_bar.Hide()
        super()._onLeave(e)
        return
    pass

class ComboPopDiv(wx.ComboPopup):
    def __init__(self,host,**argkw):
        ''' Popup div for ComboDiv.
            Override buildDiv to build control in self.div.
            * Argkw div: Custom div class;'''
        super().__init__()
        self.host:ComboDiv=host
        self._argkw=argkw
        self.DivClass=argkw.get('div',Div)
        return

    def buildDiv(self):
        ''' Empty method. Avaiable for overriding.'''
        return

    def getComboDiv(self):
        cd:ComboDiv=self.GetComboCtrl()
        return cd

    def setPopupSize(self,**argkw):
        ''' Set div size in popup.
            * Argkw s: size tuple;
            * Argkw h: height;
            * Argkw w: width;'''
        if 's' in argkw:s=argkw['s']
        else:
            w=self._argkw['style']['s'][0]
            h=self._argkw['style']['s'][1]
            if 'w' in argkw:w=argkw['w']
            if 'h' in argkw:h=argkw['h']
            s=(w,h)
        self._argkw['style']['s']=s
        self.div.SetSize(s)
        self.host.SetPopupMinWidth(s[0])
        self.host.SetPopupMaxHeight(s[1])
        return

    def Create(self,parent):
        # Overrided;
        self.div=self.DivClass(parent,**self._argkw)
        self.div.delChildren()
        self.buildDiv()
        return True

    def GetControl(self):
        # Overrided;
        return self.div

    def GetStringValue(self):
        # Overrided;
        return str()

    def OnDismiss(self):
        # Overrided;
        cdiv:ComboDiv=self.GetComboCtrl()
        cdiv._flag_enable=True
        cdiv.setActive(False)
        wx.ComboPopup.OnDismiss(self)
        return
    pass
class ComboDiv(DivBase,wx.ComboCtrl):
    def __init__(self, parent: wx.Window, **argkw):
        ''' Combo div.
            * argkw popup: Popup to set;'''
        wx.ComboCtrl.__init__(self,parent,style=wx.CB_READONLY)
        DivBase.__init__(self,parent, **argkw)
        self.popup:ComboPopDiv=None
        self._flag_enable=True
        if 'popup' in argkw:self.setPopup(argkw['popup'])
        return

    def setPopup(self,popup:ComboPopDiv):
        self.popup=popup
        self.SetPopupControl(popup)
        self.SetPopupMinWidth(popup._argkw['style']['s'][0])
        self.SetPopupMaxHeight(popup._argkw['style']['s'][1])
        return

    def bindPopup(self,evt,method):
        for child in self.popup.div.getChildren():
            child.Bind(evt,method)

    def _onClk(self, e: wx.Event):
        super()._onClk(e)
        self._flag_enable=False
        return

    def setActive(self, active=None) -> bool:
        if self._flag_enable:
            return super().setActive(active=active)
        return
    pass

class IndePopupDiv(DivBase,wx.PopupWindow):
    def __init__(self,parent,**argkw):
        wx.PopupWindow.__init__(self,parent)
        DivBase.__init__(self,parent,**argkw)
        self.SetExtraStyle(wx.PU_CONTAINS_CONTROLS)
        self.setPopupPos(self.style['p'])
        self.updateStyle(style={'border':esui.COLOR_FRONT})
        self.parent.Bind(wx.EVT_LEFT_DOWN,self._onLostFocus)
        return

    def bindPopup(self,evt,method):
        ''' Bind event for children in popup.'''
        for child in self.getChildren():
            child.Bind(evt,method)
        return

    def _onLostFocus(self,e):
        e.Skip()
        self.parent.Unbind(wx.EVT_LEFT_DOWN,handler=self._onLostFocus)
        self.DestroyLater()
        return

    def setPopupPos(self,p):
        pp=self.parent.Position
        p=(pp.x+p[0],pp.y+p[1])
        self.updateStyle(style={'p':p})
        self.Position(p,(0,0))
        return
    pass

class MenuPopup(ComboPopDiv):
    def __init__(self,host,**argkw):
        ''' Menu popup.'''
        super().__init__(host,**argkw)
        self.stl_item={'s':(argkw['style']['s'][0]*2-4*yu,3*yu),'align':'left'}
        self.stl_item_hover={'border_bottom':esui.COLOR_FRONT}
        return

    def buildDiv(self):
        self.div.delChildren()
        items=self.host.items
        for i in range(len(items)):
            self.stl_item.update({'p':(2*yu,i*4*yu+1)})
            if isinstance(items[i],str):
                item=esui.Div(self.div,label=items[i],
                    style=self.stl_item,hover=self.stl_item_hover)
                item.Bind(wx.EVT_LEFT_DOWN,self.onClkItem)
                item.popup_index=i
            else:
                'todo: itemclass'
        self.setPopupSize(w=self.host.Size.x*2,h=len(items)*4*yu)
        return

    def onClkItem(self,e:wx.Event):
        e.Skip()
        self.host.value=e.EventObject.label
        if self.host.flag_select:
            self.host.setLabel(self.host.value)
        self.Dismiss()
        return
    pass
class MenuBtnDiv(ComboDiv):
    def __init__(self, parent: wx.Window, **argkw):
        ''' Menu button using div.
            * Argkw items: Accept list of str or ItemClass;
            * Argkw no_border: False default;
            * Argkw select: False default for not selecting item to button;'''
        self.value=''
        self.items=argkw.get('items',list())
        self.flag_select=argkw.get('select',False)
        argkw['hover']={'bgc':esui.COLOR_HOVER}
        argkw['active']={'bgc':esui.COLOR_FRONT,'text':esui.COLOR_BLACK}
        if 'border' not in argkw['style']:
            argkw['style'].update({'border':esui.COLOR_FRONT})
        if argkw.get('no_border',False):
            del argkw['style']['border']
            argkw['style']['bgc']=esui.COLOR_LBACK
        pop=MenuPopup(self,style={'border':esui.COLOR_FRONT,'s':argkw['style']['s']})

        super().__init__(parent, popup=pop,**argkw)
        return

    def _onPaint(self, e):
        super()._onPaint(e)
        if 'border' in self.style:
            dc=wx.PaintDC(self)
            dc.SetPen(wx.Pen(self.style['border']))
            dc.SetBrush(wx.Brush(self.style['border']))
            dc.DrawPolygon([
                (self.Size.x,self.Size.y),
                (self.Size.x-yu,self.Size.y),
                (self.Size.x,self.Size.y-yu)
            ])
        return

    def setItems(self,items):
        self.items=items
        self.popup.buildDiv()
        return

    def getCurrent(self):
        return self.value
    pass
