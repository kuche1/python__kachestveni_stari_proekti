
al = []

class a():
    name = 'ERROR'
    desc = 'nz'
    hpmax = 100
    speed = 5
    camspeed = 2
    detectrange = 1000
    clipmult = 1
    ammomult = 1
    rlmult = 1
    frmult = 1
    dmgmult = 1
    bpsmult = 1
    explradmult = 1
    meledmgmult = 1
    melefrmult = 1
    costmult = 1
    guns = ['rifle']

class theflash(a):
    name = 'The Falsh'
    desc = 'Bari Alen'
    

class test(a):
    name = 'Test'
    desc = 'nz'
    hpmax = 1000
    speed = 10
    camspeed = 10
    detectrange = 100
al.append(test)

class berserker(a):
    name = 'Berserker'
    desc = '6lqpa6 gi mnogo'
    hpmax = 200
    speed = 8
    camspeed = 3
    detectrange = 600
    clipmult = 1.2
    ammomult = 1.2
    rlmult = 1
    frmult = 1
    dmgmult = 1.2
    bpsmult = 1
    explradmult = 1.2
    meledmgmult = 1.5
    melefrmult = 0.7
    costmult = 0.7
    guns = ['mele']
al.append(berserker)

class gunslinger(a):
    name = 'Gunslinger'
    desc = 'polzva pi6aci'
    hpmax = 100
    speed = 7
    camspeed = 3
    detectrange = 900
    ammomult = 1.1
    rlmult = 0.6
    frmult = 1.2
    dmgmult = 1.5
    costmult = 0.8
    guns = ['pistol']
al.append(gunslinger)

class commando(a):
    name = 'Commando'
    desc = 'Ima emka'
    hpmax = 100
    speed = 5
    camspeed = 2
    detectrange = 1000
    clipmult = 1
    ammomult = 1
    rlmult = 0.8
    frmult = 1
    dmgmult = 1.2
    bpsmult = 1
    explradmult = 1
    costmult = 0.8
    guns = ['rifle']
al.append(commando)

class demolitionist(a):
    name = 'Demolitionist'
    desc = 'Bym bym'
    hpmax = 100
    speed = 5
    camspeed = 3
    clipmult = 1
    ammomult = 1.2
    rlmult = 0.7
    frmult = 1
    dmgmult = 1.6
    bpsmult = 1.1
    explradmult = 3
    costmult = 0.7
    guns = ['explosive']
al.append(demolitionist)    

class thearrow(a):
    name = 'Da strelata'
    desc = 'Ima luk ako ne zabrava da go adna v igrata'
    hpmax = 101
    speed = 4.5
    camspeed = 4
    detectrange = 800
    clipmult = 1
    ammomult = 1.4
    rlmult = 1
    frmult = 1
    dmgmult = 1
    bpsmult = 1
    explradmult = 3
    costmult = 0.8
    guns = ['crossbow', 'bow']
al.append(thearrow)

class scout(a):
    name = 'Scout'
    desc = 'Fast es fk'
    hpmax = 80
    speed = 8
    camspeed = 4
    frmult = 0.8
    dmgmult = 1
    explradmult = 1.2
    costmult = 0.6
    guns = []
al.append(scout)

class support(a):
    name = 'Support'
    desc = 'Ima pompa'
    hpmax = 140
    speed = 4
    camspeed = 2
    clipmult = 1.1
    ammomult = 1.3
    rlmult = 1.3
    frmult = 1
    dmgmult = 1
    bpsmult = 1.5
    explradmult = 1.1
    costmult = 0.9
    guns = ['shotgun']
al.append(support)

class treidarbg(a):
    name = 'Traider.bg'
    desc = 'Nai-dobriq sait za pokupka i prodajba na stoki v bulgariq'
    clipmult = 0.9
    ammomult = 0.9
    rlmul1 = 1.1
    frmult = 1.1
    dmgmult = 0.9
    bpsmult = 0.9
    explradmult = 0.9
    costmult = 0.6
    guns = ['all']
al.append(treidarbg)
