from threading import Thread
import pymem
from Offsets import *
from win32api import GetAsyncKeyState
import keyboard
from math import sqrt, pi, atan
import time
from win32gui import GetWindowText, GetForegroundWindow
 
 
smooth = int(input('Set Smooth Value(1-2000)'))
aimfov = int(input('Set Fov Value(1-26)'))
name_check = GetWindowText(GetForegroundWindow())
cs_name = "Counter-Strike: Global Offensive"
 
 
try:
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    enginepointer = pm.read_int(engine + dwClientState)
except pymem.exception.ProcessNotFound:
    print('Launch Game')
    quit()
 
def Set_VA(X, Y):
    pm.write_float(enginepointer + dwClientState_ViewAngles, X)
    pm.write_float(enginepointer + dwClientState_ViewAngles + 0x4, Y)
def resendpackers():
    while True:
        time.sleep(0.1)
        pm.write_uchar(engine + dwbSendPackets, 1)
Thread(target=resendpackers).start()
def radar():
    while True:
        try:
            if pm.read_int(client + dwLocalPlayer):
                localplayer = pm.read_int(client + dwLocalPlayer)
                localplayer_team = pm.read_int(localplayer + m_iTeamNum)
                for i in range(64):
                    if pm.read_int(client + dwEntityList + i * 0x10):
                        entity = pm.read_int(client + dwEntityList + i * 0x10)
                        entity_team = pm.read_int(entity + m_iTeamNum)
                        if entity_team != localplayer_team:
                            pm.write_int(entity + m_bSpotted, 1)
        except:
            pass
Thread(target=radar).start()
 
def buny():
    while True:
        try:
            name_check = GetWindowText(GetForegroundWindow())
            if pm.read_int(client + dwLocalPlayer) and name_check == cs_name:
                player = pm.read_int(client + dwLocalPlayer)
                force_jump = client + dwForceJump
                on_ground = pm.read_int(player + m_fFlags)
                velocity = pm.read_float(player + m_vecVelocity)
                if keyboard.is_pressed("space") and on_ground == 257:
                    if velocity < 1 and velocity > -1:
                        pass
                    else:
                        pm.write_int(force_jump, 5)
                        time.sleep(0.17)
                        pm.write_int(force_jump, 4)
        except:
            pass
Thread(target=buny).start()
def rcs():
    oldpunchx = 0.0
    oldpunchy = 0.0
    while True:
        try:
            name_check = GetWindowText(GetForegroundWindow())
            if pm.read_int(client + dwLocalPlayer) and name_check == cs_name:
                rcslocalplayer = pm.read_int(client + dwLocalPlayer)
                rcsengine = pm.read_int(engine + dwClientState)
                if pm.read_int(rcslocalplayer + m_iShotsFired) > 2:
                    rcs_x = pm.read_float(rcsengine + dwClientState_ViewAngles)
                    rcs_y = pm.read_float(rcsengine + dwClientState_ViewAngles + 4)
                    punchx = pm.read_float(rcslocalplayer + m_aimPunchAngle)
                    punchy = pm.read_float(rcslocalplayer + m_aimPunchAngle + 4)
                    newrcsx = rcs_x - (punchx - oldpunchx) * 2
                    newrcsy = rcs_y - (punchy - oldpunchy) * 2
                    oldpunchx, oldpunchy = punchx, punchy
                    if checkangles(newrcsx, newrcsy):
                        pm.write_float(rcsengine + dwClientState_ViewAngles, newrcsx)
                        pm.write_float(rcsengine + dwClientState_ViewAngles + 0x4, newrcsy)
                else:
                    oldpunchx = 0.0
                    oldpunchy = 0.0
        except:
            pass
Thread(target=rcs).start()
 
def GlowESP():
    while True:
        try:
            name_check = GetWindowText(GetForegroundWindow())
            if pm.read_int(client + dwLocalPlayer) and name_check == cs_name:
                localplayer = pm.read_int(client + dwLocalPlayer)
                localplayer_team = pm.read_int(localplayer + m_iTeamNum)
                localplayer_index = pm.read_int(localplayer + 0x64) - 1
                for x in range(64):
                    if pm.read_int(client + dwEntityList + x * 0x10):
                        entity = pm.read_int(client + dwEntityList + x * 0x10)
                        spotted = pm.read_int(entity + m_bSpottedByMask)
                        entity_team = pm.read_int(entity + m_iTeamNum)
                        glow_manager = pm.read_int(client + dwGlowObjectManager)
                        entity_glow = pm.read_int(m_iGlowIndex + entity)
                        if entity and entity_team != localplayer_team:
                            if spotted == 1 << localplayer_index:
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, 0.5)  # B
                            else:
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, 0.5)  # G
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, 1.0)
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
        except:
            pass
Thread(target=GlowESP).start()
 
 
 
def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
 
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey
def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True
def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY
def Distance(src_x, src_y, src_z, dst_x, dst_y, dst_z):
    try:
        diff_x = src_x - dst_x
        diff_y = src_y - dst_y
        diff_z = src_z - dst_z
        return sqrt(diff_x * diff_x + diff_y * diff_y + diff_z * diff_z)
    except:
        pass
def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    try:
        delta_x = localpos1 - enemypos1
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except:
        pass
def Aimbot():
    while True:
        try:
            name_check = GetWindowText(GetForegroundWindow())
            olddistx = 111111111111
            olddisty = 111111111111
            target = None
            aimlocalplayer = pm.read_int(client + dwLocalPlayer)
            if aimlocalplayer and name_check == cs_name:
                global localplayer_team
                localplayer_team = pm.read_int(aimlocalplayer + m_iTeamNum)
                for x in range(32):
                    if pm.read_int(client + dwEntityList + x * 0x10):
                        entity = pm.read_int(client + dwEntityList + x * 0x10)
                        entity_hp = pm.read_int(entity + m_iHealth)
                        entity_team = pm.read_int(entity + m_iTeamNum)
                        if localplayer_team != entity_team and entity_hp > 0:
                            entity_bones = pm.read_int(entity + m_dwBoneMatrix)
                            localpos_x_angles = pm.read_float(enginepointer + dwClientState_ViewAngles)
                            localpos_y_angles = pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
                            localpos1 = pm.read_float(aimlocalplayer + m_vecOrigin)
                            localpos2 = pm.read_float(aimlocalplayer + m_vecOrigin + 4)
                            localpos_z_angles = pm.read_float(aimlocalplayer + m_vecViewOffset + 0x8)
                            localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + localpos_z_angles
                            entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xC)
                            entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1C)
                            entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2C)
                            X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                            newdist_x, newdist_y = calc_distance(localpos_x_angles, localpos_y_angles, X, Y)
                            if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= aimfov and newdist_y <= aimfov:
                                olddistx, olddisty = newdist_x, newdist_y
                                target, target_hp = entity, entity_hp
                                target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z
                if target and target_hp > 0 and GetAsyncKeyState(18) != 0:
                    x, y = calcangle(localpos1, localpos2, localpos3, target_x, target_y, target_z)
                    normalize_x, normalize_y = normalizeAngles(x, y)
                    silent(normalize_x, normalize_y)
        except:
            pass
def silent(x, y):
    pm.write_uchar(engine + dwbSendPackets, 0)
    Commands = pm.read_int(client + dwInput + 0xF4)
    VerifedCommands = pm.read_int(client + dwInput + 0xF8)
    Desired = pm.read_int(enginepointer + clientstate_last_outgoing_command) + 2
    OldUser = Commands + ((Desired - 1) % 150) * 100
    VerifedOldUser = VerifedCommands + ((Desired - 1) % 150) * 0x68
    m_buttons = pm.read_int(OldUser + 0x30)
    Net_Channel = pm.read_uint(enginepointer + clientstate_net_channel)
    if pm.read_int(Net_Channel + 0x18) >= Desired:
        pm.write_float(OldUser + 0x0C, x)
        pm.write_float(OldUser + 0x10, y)
        pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
        pm.write_float(VerifedOldUser + 0x0C, x)
        pm.write_float(VerifedOldUser + 0x10, y)
        pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
        pm.write_uchar(engine + dwbSendPackets, 1)
Thread(target=Aimbot).start()
def GetVM():
    VMatrix = [0] * 16
    for x in range(16):
        VMatrix[x] = pm.read_float((client + dwViewMatrix) + (x * 0x4))
    return VMatrix
def W2S(matrix, x, y, z, Width, Height):
    while True:
        clX = x * matrix[0] + y * matrix[1] + z * matrix[2] + matrix[3]
        clY = x * matrix[4] + y * matrix[5] + z * matrix[6] + matrix[7]
        clW = x * matrix[12] + y * matrix[13] + z * matrix[14] + matrix[15]
        if clW > 0.1:
            nX = clX / clW
            nY = clY / clW
            screen_x = (Width / 2 * nX) + (nX + Width / 2)
            screen_y = -(Height / 2 * nY) + (nY + Height / 2)
            return screen_x, screen_y
        else:
            return 960, 1080