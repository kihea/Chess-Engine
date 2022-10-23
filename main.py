from cmu_graphics import *

import math, time


class Status:
    status = 0


class Active(Status):
    status = 1

    def __neg__(self):
        return Inactive()


class Inactive(Status):
    status = 4

    def __neg__(self):
        return Active()


class Paused(Status):
    status = 3

    def __neg__(self):
        return Loading()


class Loading(Status):
    status = 2

    def __neg__(self):
        return Paused()


class InterfaceManager:
    stack = []

    def push(self, UI):
        self.stack.insert(0, UI)

    def pop(self):
        return self.stack.pop(0)

    def keyPress(self, key):
        pass

    def clear(self):
        for ui in self.stack:
            ui.Interface.clear()
        self.stack = []


interface = app.InterfaceManager = InterfaceManager()


class InterfaceBase:
    Interface = Group()
    SinkInput = False

    def onActivate(self):
        pass


class Button(InterfaceBase):
    status = Inactive()
    SinkInput = True

    def __init__(self,
                 look,
                 x,
                 y,
                 actiFunc,
                 l=30,
                 w=10,
                 r=10,
                 text="",
                 scaleText=True,
                 backgroundColor=rgb(255, 255, 255),
                 textColor=rgb(0, 0, 0),
                 funcInp=None):
        if look == "simple":
            shadow = Rect(x - 1, y + 1, l, w, fill="grey", opacity=30)
            main = Rect(x, y, l, w, fill=backgroundColor)

            self.Interface.add(
                shadow, main,
                Label(text,
                      x + l // 2,
                      y + w // 2,
                      fill=textColor,
                      size=w // 4))
            self.Interface.mainButton = main
        elif look == "circular":
            main = Circle(x, y, r, fill=backgroundColor, border="black")
            self.Interface.add(main, Label("+", x, y, fill=textColor, size=r))
            self.Interface.mainButton = main
        self.style = look
        self.activationFunc = actiFunc
        self.funcInp = funcInp
        interface.push(self)

    def enable(self):
        self.status = Inactive()

    def onActivate(self):
        if type(self.status) is Active or self.Interface.visible == False:
            return
        self.status = Active()
        if self.style == "simple":
            handler.newAnim(
                self.Interface.mainButton,
                "centerX",
                self.Interface.mainButton.centerX - 2,
                0.25,
                "linear",
                coanims=[
                    handler.newAnim(self.Interface.mainButton,
                                    "centerY",
                                    self.Interface.mainButton.centerY + 2,
                                    0.25,
                                    "linear",
                                    linkedAnimations=[
                                        handler.newAnim(
                                            self.Interface.mainButton,
                                            "centerY",
                                            self.Interface.mainButton.centerY,
                                            0.1, "linear")
                                    ])
                ],
                linkedAnimations=[
                    handler.newAnim(self.Interface.mainButton, "centerX",
                                    self.Interface.mainButton.centerX, 0.1,
                                    "linear")
                ],
                onFinish=self.enable)
        elif self.style == "circular":
            handler.newAnim(self.Interface.mainButton,
                            "radius",
                            self.Interface.mainButton.radius + 3,
                            .5,
                            "elasticOut",
                            linkedAnimations=[
                                handler.newAnim(
                                    self.Interface.mainButton, "radius",
                                    self.Interface.mainButton.radius, 1,
                                    "elasticIn")
                            ],
                            onFinish=self.enable)
        if self.funcInp:

            self.activationFunc(self.funcInp)
        else:
            self.activationFunc()


class Checkbox(InterfaceBase):
    status = Active()

    def __init__(self, x, y, size, color=rgb(0, 0, 0)):
        self.size = size * .8
        self.back = Circle(x,
                           y,
                           size,
                           border="grey",
                           borderWidth=1,
                           fill="white")
        self.uiA = Circle(x, y, self.size, fill=color)
        self.Interface.add(
            self.back,
            self.uiA,
        )
        interface.push(self)

    def onActivate(self):
        if type(self.status) is Active:
            handler.newAnim(self.uiA,
                            "radius",
                            1,
                            .05,
                            "quadIn",
                            onFinish=self.toggle)
        else:
            handler.newAnim(self.uiA,
                            "radius",
                            self.size,
                            .3,
                            "linear",
                            onFinish=self.toggle)

    def toggle(self):
        if type(self.status) is Active:
            self.uiA.opacity = 0
            self.status = Inactive()
        else:
            self.uiA.opacity = 100
            self.status = Active()


class Toggle(InterfaceBase):
    pass


class ProgressBar(InterfaceBase):
    pass


class CircleLoader(InterfaceBase):
    def __init__(self, x, y, radius, color, fillColor=rgb(255, 255, 255)):
        self.Loader = Arc(x, y, radius, radius, 0, 1, fill=color)
        self.Interface.add(self.Loader,
                           Circle(x, y, radius - 25, fill=fillColor))
        manager.bindToFixedStep(str(id(self)), self.start)

    def reset(self):
        self.Loader.sweepAngle = 1

    def start(self):
        handler.newAnim(self.Loader,
                        "sweepAngle",
                        360,
                        1,
                        "expInOut",
                        frozen=False,
                        transform=lambda x: int(x),
                        before=self.reset)


class TextBox(InterfaceBase):
    pass


class AppManager:
    active = None
    apps = []
    binds = {}
    status = Inactive()
    loaderApp = None
    homeApp = None

    def startApp(self, app):
        self.terminateApp(self.active)
        self.active = app
        self.bindToFixedStep("active", app.fixedStep)
        app.status = Active()
        app.onStart()

    def step(self):
        if not self.active:
            return
        self.active.step()

        if int(app.elapsed) % 3 == 0:
            #self.active.fixedStep()
            for function in self.binds.values():
                function()

    def keyPress(self, key):
        if key == "escape":
            self.startApp(self.homeApp)

    def mouseDrag(self, x, y):
        if self.active:
            self.active.onDrag(x, y)

    def mouseRelease(self, x, y):
        if self.active:
            self.active.onMouseRelease(x, y)

    def mousePress(self, x, y):
        if self.active:
            self.active.onMousePress(x, y)

    def bindToFixedStep(self, name, function):
        self.binds[name] = function

    def unbindFromFixedStep(self, name):
        del self.binds[name]

    def terminateApp(self, app):
        if not app:
            return

        app.status = Inactive()
        app.Interface.clear()
        interface.clear()
        self.active = None
        self.unbindFromFixedStep("active")
        app.terminate()

    def initiate(self):
        self.status = Loading()
        self.startApp(self.loaderApp)

    def loadApp(self, app):
        self.apps.append(app)

    def setLoadApp(self, app):
        self.loaderApp = app

    def setHomeApp(self, app):
        self.homeApp = app

    def getApps(self, exclude):
        return filter(lambda x: not x in [*exclude, self.loaderApp], self.apps)


def onMousePress(x, y):
    for ui in interface.stack:
        if ui.Interface.hits(x, y):
            ui.onActivate()
            if ui.SinkInput:
                return
            continue
    manager.mousePress(x, y)


app.reservedKeys = ['escape']


def onKeyPress(key):
    if key in app.reservedKeys:
        manager.keyPress(key)
        return
    interface.keyPress(key)


def onMouseDrag(x, y):
    manager.mouseDrag(x, y)


def onMouseRelease(x, y):
    manager.mouseRelease(x, y)


class App:
    status = Inactive()

    def __init__(self, cacheData={}):
        self.Interface = Group()
        self.cache = cacheData
        pass

    def terminate(self):
        self.Interface.clear()
        self.onTerminate()

    def start(self):
        self.isOpen = True
        self.group = Group()
        self.onStart()

    def step(self):
        ##
        self.onStep()

    def onStart(self):
        pass

    def onTerminate(self):
        pass

    def onStep(self):
        pass

    def fixedStep(self):
        pass

    def onDrag(self, x, y):
        pass

    def onMouseRelease(self, x, y):
        pass

    def onMousePress(self, x, y):
        pass


class Queue:
    stack = []

    def push(self, value, att=0):
        value.__ATTEMPTNUM = att
        self.stack.append(value)

    def advance(self):
        if len(self.stack) > 0:
            t = self.stack.pop(0)

            done = t.frame()
            if done:
                return
            self.push(t, att=0)

    def flush(self):
        for i in range(len(self.stack)):
            self.advance()


##### Animation
class Animation:
    def __init__(self,
                 obj,
                 prop,
                 start,
                 end,
                 duration,
                 method,
                 limitMin=0,
                 limitMax=1,
                 frozen=False,
                 links=[],
                 coanims=[],
                 transform=lambda x: x,
                 onFinish=None,
                 before=None):
        if before:
            before()
        self.obj = obj
        self.prop = prop
        self.getstart = start
        self.start = start(obj, prop)
        self.end = end
        self.duration = duration
        self.elapsed = 0.0
        self.limit = (limitMin, limitMax)
        self.func = method
        self.link = [links] if type(links) is Animation else (
            links if type(links) is list else [])
        self.coanims = [coanims] if type(coanims) is Animation else (
            coanims if type(coanims) is list else [])
        self.Frozen = frozen
        self.tfs = transform
        self.onFinish = onFinish

    def frame(self):
        if self.Frozen:
            return False
        t = self.limit[0] * (1 - self.elapsed) + self.limit[1] * self.elapsed
        t = self.elapsed / self.duration
        if t >= 1.0:
            t = 1
        interp = self.func(t)
        val = (self.end * interp) + (self.start * (1 - interp))
        setattr(self.obj, self.prop, self.tfs(val))

        if self.elapsed >= self.duration:
            self.complete()
            return True
        self.elapsed += app.delta
        return False

    def link(self, animation):
        animation.freeze()
        self.link.append(animation)

    def freeze(self):
        self.Frozen = True

    def thaw(self, links=[], finishFunc=None):
        self.start = self.getstart(self.obj, self.prop)
        self.onFinish = finishFunc
        handler.AnimQu.push(self)
        self.Frozen = False
        self.link = links

    def toggle(self):
        self.Frozen = not self.Frozen

    def complete(self):
        self.Finished = True
        self.Frozen = True

        if len(self.link) > 0:
            nextAnim = self.link.pop()
            nextAnim.thaw(links=self.link, finishFunc=self.onFinish)
        elif self.onFinish:
            self.onFinish()


class AnimationHandler:
    AnimQu = Queue()
    status = Active()

    def newAnim(self,
                obj,
                prop,
                end,
                time,
                method,
                frozen=False,
                linkedAnimations=[],
                coanims=[],
                transform=lambda x: x,
                onFinish=None,
                before=None):

        methods = [
            self.linear, self.quadIn, self.quadOut, self.quadInOut,
            self.cubicIn, self.cubicOut, self.cubicInOut, self.quartIn,
            self.quartOut, self.quartInOut, self.quintIn, self.quintOut,
            self.quintInOut, self.sineIn, self.sineOut, self.sineInOut,
            self.expIn, self.expOut, self.expInOut, self.elasticIn,
            self.elasticOut, self.elasticInOut
        ]
        methodsSTR = {
            "linear": self.linear,
            "quadIn": self.quadIn,
            "quadOut": self.quadOut,
            "quadInOut": self.quadInOut,
            "cubicIn": self.cubicIn,
            "cubicOut": self.cubicOut,
            "cubicInOut": self.cubicInOut,
            "quintIn": self.quintIn,
            "quintOut": self.quintOut,
            "quintInOut": self.quintInOut,
            "quartIn": self.quartIn,
            "quartOut": self.quartOut,
            "quartInOut": self.quartInOut,
            "expIn": self.expIn,
            "expOut": self.expOut,
            "expInOut": self.expInOut,
            "sineIn": self.sineIn,
            "sineOut": self.sineOut,
            "sineInOut": self.sineInOut,
            "elasticIn": self.elasticIn,
            "elasticOut": self.elasticOut,
            "elasticInOut": self.elasticInOut,
        }
        if type(method) is str:
            ref = methodsSTR[method]
        elif type(method) is int:
            ref = methods[method]
        else:
            raise TypeError("Illegal type " + str(type(method)))
        ani = Animation(obj,
                        prop,
                        lambda x, y: getattr(x, y),
                        end,
                        time,
                        ref,
                        frozen=frozen,
                        links=linkedAnimations,
                        coanims=coanims,
                        transform=transform,
                        onFinish=onFinish,
                        before=before)
        self.AnimQu.push(ani)
        for anim in linkedAnimations:
            anim.masterAnimation = ani
        return ani

    def linkAnim(self, anim1, anim2):
        if anim2.masterAnimation:
            return
        anim1.link(anim2)

    def advance(self):
        self.AnimQu.flush()

    def linear(self, x):
        return x

    def quadIn(self, x):
        return x**2

    def quadOut(self, x):
        return -(x * (x - 2))

    def quadInOut(self, x):
        if x < 0.5:
            return 2 * (x**2)
        return ((-2 * (x**2)) + (4 * x) - 1)

    def cubicIn(self, x):
        return x**3

    def cubicOut(self, x):
        return (x - 1)**3 + 1

    def cubicInOut(self, x):
        if t < 0.5:
            return 4 * x**3
        p = 2 * x - 2
        return 0.5 * p**3 + 1

    def quartIn(self, x):
        return x**4

    def quartOut(self, x):
        return 1 - (1 - x)**4

    def quartInOut(self, x):
        if t < 0.5:
            return 8 * x**4
        p = x - 1
        return -8 * p**4 + 1

    def quintIn(self, x):
        return x * x * x * x * x

    def quintOut(self, x):
        return (x - 1)**5 + 1

    def quintInOut(self, x):
        if t < 0.5:
            return 16 * x**5
        p = 2 * x - 2
        return 0.5 * p**5 + 1

    def sineIn(self, x):
        return math.sin((x - 1) * math.pi / 2) + 1

    def sineOut(self, x):
        return math.sin(x + math.pi / 2)

    def sineInOut(self, x):
        return 0.5 * (1 - math.cos(x * math.pi))

    def expOut(self, x):
        if x == 1:
            return 1
        return 1 - 2**(-10 * x)

    def expIn(self, x):
        if x == 0:
            return 0
        return 2**(10 * (x - 1))

    def expInOut(self, x):
        if x == 0 or x == 1:
            return x
        if x < 0.5:
            return 2**(20 * x - 10) / 2
        return (2 - 2**(-20 * x + 10)) / 2

    def elasticOut(self, x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        const = (2 * math.pi) / 3
        return 2**(-10 * x) * math.sin((x * 10 - 0.75) * const) + 1

    def elasticIn(self, x):
        if x == 0:
            return 0
        elif x == 1:
            return 1

        const = (2 * math.pi) / 3
        return -2**(10 * x - 10) * math.sin((x * 10 - 10.75) * const)

    def elasticInOut(self, x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        const = (2 * math.pi) / 4.5
        if x < 0.5:
            return -(2**(20 * x - 10) * math.sin(
                (20 * x - 11.125) * const)) / 2
        else:
            return -(2**(-20 * x + 10) * math.sin(
                (20 * x - 11.125) * const)) / 2 + 1


##### Define Globals
manager = app.AppManager = AppManager()
handler = app.AnimationHandler = AnimationHandler()

app.prevFrameTime = time.time()
app.elapsed = 0.0
app.stepsPerSecond = 120  #fps


def onStep():
    app.delta = time.time() - app.prevFrameTime
    app.prevFrameTime = time.time()
    app.elapsed += app.delta
    if manager.active:
        manager.step()
    if type(handler.status) is Active:
        handler.advance()


class LScreen(App):
    def onStart(self):
        self.label = Label("AppZen",
                           800,
                           80,
                           font="orbitron",
                           bold=True,
                           size=20)
        handler.newAnim(self.label,
                        "centerX",
                        200,
                        2,
                        "elasticOut",
                        onFinish=self.startHome)
        self.Interface.add(self.label)
        #self.Loader = CircleLoader(200, 280, 35, rgb(0,0,0))

    def startHome(self):
        manager.startApp(manager.homeApp)


class HomeScreen(App):
    gridsize = 80
    buttonsize = 60
    padding = 20
    ypadding = 60
    lrpadding = 10

    def onStart(self):  #fired after load screen is destroyed
        self.Interface.add(Label("APPZEN", 200, 60, size=20, bold=True))
        app.background = rgb(200, 200, 200)
        for i, appli in enumerate(manager.getApps([self])):
            maxGrid = (400 - self.lrpadding) // (self.buttonsize +
                                                 self.padding)
            #Rect((i % maxGrid) * self.gridsize + self.padding, (i // maxGrid) * self.gridsize + self.ypadding + 100, self.gridsize, self.gridsize, fill = None, border = "black") VISUALIZE GRID
            Button("simple", (i % maxGrid) * self.gridsize + self.padding +
                   (0.125 * self.gridsize), (i // maxGrid) * self.gridsize +
                   self.ypadding + 100 + (0.125 * self.gridsize),
                   manager.startApp,
                   text=appli.name,
                   funcInp=appli,
                   l=self.buttonsize,
                   w=self.buttonsize)


class Move:
    target = None
    start = None
    done = False
    flags = {'promotion': False}

    def __init__(self, start, target, capture=False, promotion=False):

        self.target = target
        self.start = start
        self.flags = {'capture': capture, 'promotion': promotion}

    def __str__(self):
        return str(self.start) + " -> " + str(self.target)

    def __repr__(self):
        return str(self)


class Piece:
    inOriginalPosition = True
    isPinned = False
    isTaken = False

    def __init__(self, row, col, side, useBackups=False):
        self.side = side
        if not useBackups:
            try:
                if side == 0:
                    self.image = Image(self.imageWhite,
                                       col * 40 + 40,
                                       row * 40 + 40,
                                       fill=None,
                                       height=40,
                                       width=40)
                else:
                    self.image = Image(self.imageBlack,
                                       col * 40 + 40,
                                       row * 40 + 40,
                                       fill=None,
                                       height=40,
                                       width=40)
            except:
                useBackups = True
                self.image = Label(self.backUp,
                                   col * 40 + 60,
                                   row * 40 + 60,
                                   fill="white" if side == 0 else "black",
                                   size=30)
        else:
            self.image = Label(self.backUp,
                               col * 40 + 60,
                               row * 40 + 60,
                               fill="white" if side == 0 else "black",
                               size=30)
        self.row = row
        self.col = col
        self.position = (row, col)

    def move(self, piece):
        if type(piece) is tuple:
            row, col = piece[0], piece[1]
        elif issubclass(type(piece), Piece):
            row, col = piece.row, piece.col
        self.row = row
        self.col = col
        self.position = (row, col)

    def getPos(self):
        return (self.row, self.col)

    def capture(self):
        self.image.visible = False

    def __str__(self):
        return self.backUp


class Pawn(Piece):
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Chess_plt45.svg/45px-Chess_plt45.svg.png"
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Chess_pdt45.svg/45px-Chess_pdt45.svg.png"
    backUp = 'P'

    def genMoves(self, board):
        possibleMoves = []
        promotion = False

        row, col = self.position[0], self.position[1]
        advancedPosition = row + (-1 if self.side == 0 else 1)
        if advancedPosition == 0 or advancedPosition == 7:
            promotion = True
        attackingPositions = [(advancedPosition, col + 1),
                              (advancedPosition, col - 1)]

        if row == 1 and self.side == 1:
            possibleMoves.append(Move(self.position, (row + 2, col)))
        elif row == 6 and self.side == 0:
            possibleMoves.append(Move(self.position, (row - 2, col)))

        if not board.pieceAt(advancedPosition, col):
            possibleMoves.append(
                Move(self.position, (advancedPosition, col),
                     promotion=promotion))
        for pos in attackingPositions:
            ax, ay = pos[0], pos[1]
            if not 0 <= ax <= 7 or not 0 <= ay <= 7:
                continue

            pieceAttacking = board.pieceAt(ax, ay)

            if not pieceAttacking:
                continue
            if pieceAttacking.side == self.side:
                continue

            possibleMoves.append(
                Move(self.position, pos, capture=True, promotion=promotion))

        return possibleMoves

    def promote(self):
        pass


class Rook(Piece):
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Chess_rlt45.svg/45px-Chess_rlt45.svg.png"
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Chess_rdt45.svg/45px-Chess_rdt45.svg.png"
    backUp = 'R'

    def genMoves(self, board):

        possibleMoves = []
        row, col = self.position[0], self.position[1]

        for pos in range(row - 1, -1, -1):
            piece = board.pieceAt(pos, col)
            if piece:
                if piece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (pos, col), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (pos, col)))
        for pos in range(row + 1, 8):
            piece = board.pieceAt(pos, col)
            if piece:
                if piece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (pos, col), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (pos, col)))
        for pos in range(col - 1, -1, -1):
            piece = board.pieceAt(row, pos)
            if piece:
                if piece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (row, pos), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (row, pos)))
        for pos in range(col + 1, 8):
            piece = board.pieceAt(row, pos)
            if piece:
                if piece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (row, pos), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (row, pos)))
        return possibleMoves


class Bishop(Piece):
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Chess_blt45.svg/45px-Chess_blt45.svg.png"
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Chess_bdt45.svg/45px-Chess_bdt45.svg.png"
    backUp = 'B'

    def genMoves(self, board):
        possibleMoves = []
        row, col = self.position[0], self.position[1]

        for pos in range(row - 1, -1, -1):
            drow, dcol = pos, col - (row - pos)
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                break
            if dpiece:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        for pos in range(row + 1, 8):
            drow, dcol = pos, col + (pos - row)
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                break
            if dpiece:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        for pos in range(col - 1, -1, -1):
            drow, dcol = row + (col - pos), pos

            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                break
            if dpiece:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        for pos in range(col + 1, 8):
            drow, dcol = row - (pos - col), pos
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                break
            if dpiece:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                break
            else:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        return possibleMoves


class Knight(Piece):
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Chess_nlt45.svg/45px-Chess_nlt45.svg.png"
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Chess_ndt45.svg/45px-Chess_ndt45.svg.png"
    backUp = 'Kn'

    def genMoves(self, board):
        possibleMoves = []
        row, col = self.position[0], self.position[1]
        moves = [(row + 2, col + 1), (row + 2, col - 1), (row + 1, col + 2),
                 (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2),
                 (row - 2, col + 1), (row - 2, col - 1)]
        for move in moves:
            r, c = move[0], move[1]
            if not 0 <= r <= 7 or not 0 <= c <= 7:
                continue
            piece = board.pieceAt(r, c)
            if not piece:
                possibleMoves.append(Move(self.position, move))
            elif piece and piece.side != self.side:
                possibleMoves.append(Move(self.position, move, capture=True))
        return possibleMoves


class Queen(Piece):
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Chess_qlt45.svg/45px-Chess_qlt45.svg.png"
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Chess_qdt45.svg/45px-Chess_qdt45.svg.png"
    backUp = 'Q'

    def genMoves(self, board):
        possibleMoves = []
        row, col = self.position[0], self.position[1]
        breakVert = False
        breakS = False
        for pos in range(row - 1, -1, -1):
            spiece = board.pieceAt(pos, col)
            drow, dcol = pos, col - (row - pos)
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                dpiece = None
                breakVert = True
            if spiece and not breakS:
                if spiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (pos, col), capture=True))
                breakS = True
            elif not spiece and not breakS:
                possibleMoves.append(Move(self.position, (pos, col)))
            if dpiece and not breakVert:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                breakVert = True
            elif not dpiece and not breakVert:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        breakVert = False
        breakS = False
        for pos in range(row + 1, 8):
            #print(row, side)
            spiece = board.pieceAt(pos, col)
            drow, dcol = pos, col + (pos - row)
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                dpiece = None
                breakVert = True
            if spiece and not breakS:
                if spiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (pos, col), capture=True))
                breakS = True
            elif not spiece and not breakS:
                possibleMoves.append(Move(self.position, (pos, col)))
            if dpiece and not breakVert:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                breakVert = True
            elif not dpiece and not breakVert:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        breakVert = False
        breakS = False
        for pos in range(col - 1, -1, -1):
            spiece = board.pieceAt(row, pos)
            drow, dcol = row + (col - pos), pos

            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                breakVert = True
            if spiece and not breakS:
                if spiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (row, pos), capture=True))
                breakS = True
            elif not spiece and not breakS:
                possibleMoves.append(Move(self.position, (row, pos)))
            if dpiece and not breakVert:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                breakVert = True
            elif not dpiece and not breakVert:
                possibleMoves.append(Move(self.position, (drow, dcol)))
        breakVert = False
        breakS = False
        for pos in range(col + 1, 8):
            spiece = board.pieceAt(row, pos)
            drow, dcol = row - (pos - col), pos
            if 0 <= drow <= 7 and 0 <= dcol <= 7:
                dpiece = board.pieceAt(drow, dcol)
            else:
                breakVert = True
            if spiece and not breakS:
                if spiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (row, pos), capture=True))
                breakS = True
            elif not spiece and not breakS:
                possibleMoves.append(Move(self.position, (row, pos)))
            if dpiece and not breakVert:
                if dpiece.side != self.side:
                    possibleMoves.append(
                        Move(self.position, (drow, dcol), capture=True))
                breakVert = True
            elif not dpiece and not breakVert:
                possibleMoves.append(Move(self.position, (drow, dcol)))

        return possibleMoves


class King(Piece):
    imageBlack = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Chess_kdt45.svg/45px-Chess_kdt45.svg.png"
    imageWhite = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Chess_klt45.svg/45px-Chess_klt45.svg.png"
    backUp = 'K'

    def genMoves(self, board):
        possibleMoves = []
        row, col = self.position[0], self.position[1]
        moves = [(row + 1, col), (row, col + 1), (row, col - 1),
                 (row + 1, col + 1), (row - 1, col + 1), (row - 1, col),
                 (row + 1, col - 1), (row - 1, col - 1)]
        for move in moves:
            r, c = move[0], move[1]
            if not 0 <= r <= 7 or not 0 <= c <= 7:
                continue
            piece = board.pieceAt(r, c)
            if not piece:
                possibleMoves.append(Move(self.position, move))
            elif piece and piece.side != self.side:
                possibleMoves.append(Move(self.position, move, capture=True))
        return possibleMoves


def pr(m):
    for n in m:
        print(*n)


class Board:
    board = [[4, 2, 3, 5, 6, 3, 2, 4], [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1], [4, 2, 3, 5, 6, 3, 2, 4]]

    gridRepr = None
    turn = 0

    def move(self, move):
        if any(move.start == legal.start and move.target == legal.target
               for legal in self.psuedolegalmoves):

            x, y, tx, ty = move.start[0], move.start[1], move.target[
                0], move.target[1]
            target = self.board[tx][ty]
            start = self.board[x][y]

            start.move((tx, ty))

            if target != 0:
                target.capture()
                self.board[tx][ty] = 0
            self.board[tx][ty], self.board[x][y] = self.board[x][
                y], self.board[tx][ty]
            if 'promotion' in move.flags and move.flags['promotion']:
                target.promote()
            self.turn += 1
            self.generateMoves()
            return True

        return False

    def generateMoves(self):
        self.psuedolegalmoves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.pieceAt(row, col)
                if not piece or piece.side != self.turn % 2:
                    continue
                self.psuedolegalmoves += piece.genMoves(self)

    def pieceAt(self, x, y):
        piece = self.board[x][y]
        if piece == 0:
            return None
        return piece

    def highlightLegalMoves(self, piece, grid):
        legalMovesForPiece = list(
            filter(lambda move: move.start == piece.position,
                   self.psuedolegalmoves))
        for move in legalMovesForPiece:
            row, col = move.target[0], move.target[1]

            square = grid.hitTest(col * 40 + 60, row * 40 + 60)
            if square:
                square.border = 'blue'

    def setup(self):
        di = {1: Pawn, 2: Knight, 3: Bishop, 4: Rook, 5: Queen, 6: King}

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]
                if piece <= 0:
                    continue
                cpiece = di[piece](row, col, int(row < 4), useBackups=False)

                self.board[row][col] = cpiece

        self.generateMoves()


class Chess(App):
    name = "Chess"
    grid = Group()
    active = None
    pointedSquare = None
    board = None

    def onStart(self):

        self.makeBoard()
        self.board = Board()
        self.board.setup()

    def Turn(self, piece, color, pcx, pcy, tcx, tcy):
        pass

    def onDrag(self, x, y):
        if not self.active:
            activeSquare = self.grid.hitTest(x, y)

            if activeSquare:
                piece = self.board.pieceAt((activeSquare.top - 40) // 40,
                                           (activeSquare.left - 40) // 40)
                if piece:
                    self.active = piece.image
                    self.square = activeSquare
                    activeSquare.border = 'red'
                    for grid in self.grid:
                        if grid.border == 'blue':
                            grid.border = None
                    self.board.highlightLegalMoves(piece, self.grid)
            return
        elif self.active:
            self.active.centerX = x
            self.active.centerY = y
            target = self.grid.hitTest(x, y)

            self.pointedSquare = target
        if self.active:
            return
            a = self.grid.hitTest(x, y)
            if a and a != self.active and a != self.pointedSquare:
                if self.pointedSquare:
                    self.pointedSquare.fill = self.pointedSquare.nColor
                self.pointedSquare = a
                self.pointedSquare.fill = "yellow"

    def onMouseRelease(self, x, y):
        if self.active and self.pointedSquare:
            newSquare = self.pointedSquare

            x, y, ax, ay = (self.square.left - 40) // 40, (
                self.square.top - 40) // 40, (newSquare.left - 40) // 40, (
                    newSquare.top - 40) // 40

            move = Move((y, x), (ay, ax))
            result = self.board.move(move)
            if result:
                self.active.centerX, self.active.centerY = newSquare.centerX, newSquare.centerY
            else:
                self.active.centerX, self.active.centerY = self.square.centerX, self.square.centerY
            for grid in self.grid:
                if grid.border == 'blue':
                    grid.border = None
            self.square.border = None
            self.active = None
            self.square = None
            self.pointedSquare = None

    def onMousePress(self, x, y):

        if not self.active:
            activeSquare = self.grid.hitTest(x, y)

            if activeSquare:

                piece = self.board.pieceAt((activeSquare.top - 40) // 40,
                                           (activeSquare.left - 40) // 40)
                if piece:
                    self.active = piece.image
                    self.square = activeSquare
                    activeSquare.border = 'red'
                    for grid in self.grid:
                        if grid.border == 'blue':
                            grid.border = None
                    self.board.highlightLegalMoves(piece, self.grid)
        elif self.active:
            newSquare = self.grid.hitTest(x, y)
            x, y, ax, ay = (self.square.left - 40) // 40, (
                self.square.top - 40) // 40, (newSquare.left - 40) // 40, (
                    newSquare.top - 40) // 40

            move = Move((y, x), (ay, ax))
            result = self.board.move(move)
            if result:
                self.active.centerX, self.active.centerY = newSquare.centerX, newSquare.centerY
            else:
                self.active.centerX, self.active.centerY = self.square.centerX, self.square.centerY
            self.square.border = None
            for grid in self.grid:
                if grid.border == 'blue':
                    grid.border = None
            self.active = None
            self.square = None
            self.pointedSquare = None

    def makeBoard(self):
        for row in range(8):
            for col in range(8):
                square = Rect(40 + col * 40,
                              40 + row * 40,
                              40,
                              40,
                              fill=rgb(118, 150, 86) if
                              (row + col) % 2 == 0 else rgb(238, 238, 210))

                square.nColor = square.fill
                self.grid.add(square)

    def gridAt(self, row, col):
        return self.grid.hitCheck(col * 40 + 40, row * 40 + 40)

    def onTerminate(self):
        self.grid.clear()
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                piece = self.board.board[row][col]
                if piece != 0:
                    piece.image.visible = False
        del self.board


t = LScreen()
manager.setLoadApp(t)
manager.setHomeApp(HomeScreen())
testApp = Chess()
manager.loadApp(testApp)

manager.initiate()

cmu_graphics.run()
