class BossChernobog:
    def __init__(self):
        self.type = "CHERNOBOG"
        self.pos = pygame.Vector2(WIDTH // 2, 150)
        self.hp = 3000
        self.maxHp = 3000
        self.timer = 0
        self.hitboxRadius = 60
        self.rect = pygame.Rect(self.pos.x - 60, self.pos.y - 60, 120, 120)
        self.images = BossAssetManager.get_images("bossChernobog")
        self.currentImg = self.images["STAND"]
        
        self.orbitBullets = []
        self.orbitAngle = 0

    def update(self, eProjs, pPos):
        global shakeTimer
        self.timer += 1
        self.rect.topleft = (self.pos.x - 60, self.pos.y - 60)
        self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]
        self.orbitAngle += 0.08
        
        # 1페이즈: 궤도 탄막 응집 시간을 3배로 증가 (200 -> 600 프레임)
        if self.timer % 900 < 600:
            self.currentImg = self.images["STAND"]
            if self.timer % 5 == 0 and len(self.orbitBullets) < 120:
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), PURPLE, 15, 8)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)
                
            for i, bullet in enumerate(self.orbitBullets):
                angle = self.orbitAngle + (i * 0.15)
                radius = 70 + (i * 1.5)
                bullet.pos.x = self.pos.x + math.cos(angle) * radius
                bullet.pos.y = self.pos.y + math.sin(angle) * radius
                bullet.vel = pygame.Vector2(0, 0)
                
        # 2페이즈: 혼돈 분열 시 일부 호밍 투사체 섞기
        elif self.timer % 900 == 600:
            self.currentImg = self.images["ATTACK"]
            shakeTimer = 25 
            for bullet in self.orbitBullets:
                chaoticAngle = random.uniform(0, math.pi * 2)
                speed = random.uniform(3.0, 8.0)
                bulletVel = pygame.Vector2(math.cos(chaoticAngle), math.sin(chaoticAngle)) * speed
                
                # 15% 확률로 기존 탄막 대신 호밍 탄막 발사
                if random.random() < 0.15:
                    eProjs.append(HomingProjectile(bullet.pos.x, bullet.pos.y, bulletVel, GOLD, 15, 8))
                    if bullet in eProjs: eProjs.remove(bullet)
                else:
                    bullet.vel = bulletVel
                    bullet.color = RED 
            self.orbitBullets.clear()

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 75, self.pos.y - 75))
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GREEN, (self.pos.x - 50, self.pos.y + 80, 100 * hpRatio, 8))

class BossRock:
    def __init__(self):
        self.type = "ROCK"
        self.pos = pygame.Vector2(WIDTH // 2, 120)
        self.hp = 18000
        self.maxHp = 18000
        self.timer = 0
        self.meteors = []
        self.images = BossAssetManager.get_images("bossRock")
        self.currentImg = self.images["STAND"]
        self.phase = 1

    def _spawn_meteor(self, targetPos):
        self.meteors.append(Meteor(targetPos))

    def _explode_meteor(self, meteor, eProjs, piece_count=12, homing_count=0):
        # 메테오 폭발 시 파편(탄막) 사방으로 방출 (Danmaku 스타일)
        for angle in range(0, 360, int(360/piece_count)):
            dirVec = pygame.Vector2(0, random.uniform(3, 6)).rotate(angle)
            eProjs.append(Projectile(meteor.target.x, meteor.target.y, dirVec, RED, 8, 6))
        # 특정 페이즈에서는 폭발 시 유도 파편 추가 발생
        for _ in range(homing_count):
            eProjs.append(HomingProjectile(meteor.target.x, meteor.target.y, pygame.Vector2(random.uniform(-3,3), -3), GOLD, 10, 8))

    def update(self, eProjs, playerPos):
        self.timer += 1
        global playerHp, shakeTimer, invincibleTimer

        if self.timer < 1125: self.phase = 1
        elif self.timer < 2250: self.phase = 2
        elif self.timer < 3375: self.phase = 3
        else: self.phase = 4

        # 대지의 중압감을 표현하는 묵직한 좌우 이동
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.01) * 200 

        if self.phase == 1:
            # [기] 무차별 낙하: 운석우 + 보스의 기본 산탄
            # 패턴 1: 무작위 지역에 끊임없는 메테오
            if self.timer % 25 == 0:
                self._spawn_meteor(pygame.Vector2(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-50)))
            # 패턴 2: 보스 본체에서 발사되는 묵직한 5갈래 부채꼴 산탄
            if self.timer % 40 == 0:
                for angle in [-40, -20, 0, 20, 40]:
                    dirVec = pygame.Vector2(0, 5).rotate(angle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, GOLD, 15, 6))
            
        elif self.phase == 2:
            # [승] 정밀 타격과 화산 폭발
            # 패턴 1: 플레이어를 끈질기게 노리는 메테오
            if self.timer % 30 == 0:
                self._spawn_meteor(pygame.Vector2(playerPos.x, playerPos.y))
            # 패턴 2: 보스를 중심으로 회전하며 떨어지는 화산재 (나선탄)
            if self.timer % 5 == 0:
                angle = self.timer * 0.1
                eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, PURPLE, 10, 5))
            # 패턴 3: 십자형 파편을 남기는 대형 폭발탄 (본체에서 발사)
            if self.timer % 80 == 0:
                eProjs.append(Projectile(self.pos.x, self.pos.y, (playerPos - self.pos).normalize() * 7, CYAN, 20, 8))

        elif self.phase == 3:
            # [전] 메테오 트랩: 갇힌 공간에서의 회피
            # 패턴 1: 플레이어 주변을 포위하듯 떨어지는 3개의 메테오
            if self.timer % 50 == 0:
                for angle in [0, 120, 240]:
                    offset = pygame.Vector2(0, 120).rotate(angle + self.timer)
                    target = playerPos + offset
                    target.x = max(50, min(WIDTH-50, target.x))
                    target.y = max(50, min(HEIGHT-50, target.y))
                    self._spawn_meteor(target)
            # 패턴 2: 보스의 거대한 산탄 총 (일직선 융단 폭격)
            if self.timer % 60 == 0:
                for x_offset in range(-100, 101, 25):
                    eProjs.append(Projectile(self.pos.x + x_offset, self.pos.y, pygame.Vector2(0, 6), RED, 8, 6))
            
        elif self.phase == 4:
            # [결] 카타클리즘(대재앙): 화면 전체를 뒤덮는 메테오와 파편, 유도탄의 축제
            self.currentImg = self.images["ATTACK"]
            # 패턴 1: 초고속 랜덤 메테오 폭격
            if self.timer % 15 == 0:
                self._spawn_meteor(pygame.Vector2(random.randint(20, WIDTH-20), random.randint(50, HEIGHT-20)))
            # 패턴 2: 보스 본체의 16방향 지속 발사
            if self.timer % 15 == 0:
                for i in range(16):
                    angle = i * (math.pi / 8) + (self.timer * 0.05)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 5, CYAN, 7, 5))
            # 패턴 3: 초대형 메테오 덩어리 (같은 자리에 여러 개 동시 투하하여 폭발 파편 극대화)
            if self.timer % 90 == 0:
                target = playerPos + pygame.Vector2(random.randint(-50,50), random.randint(-50,50))
                for _ in range(3): # 3연속 낙하
                    self._spawn_meteor(target)

        # 공통 메테오 충돌 및 폭발 로직
        for meteor in self.meteors[:]:
            hitPlayer = meteor.update(playerPos)
            if hitPlayer and invincibleTimer <= 0:
                playerHp -= 25
                invincibleTimer = 40
                shakeTimer = 25
                meteor.alive = False

            if not meteor.alive:
                # 페이즈가 오를수록 파편 개수가 증가하고 유도 파편이 추가됨
                frag_count = 12 + (self.phase * 4) # 4페이즈엔 폭발당 28개의 파편
                homing = 2 if self.phase >= 3 else 0 # 3, 4페이즈엔 유도 파편 발생
                self._explode_meteor(meteor, eProjs, piece_count=frag_count, homing_count=homing)
                self.meteors.remove(meteor)

    def draw(self, surf):
        for meteor in self.meteors:
            meteor.draw(surf)
        surf.blit(self.currentImg, (self.pos.x - 50, self.pos.y - 50))
        
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 60, self.pos.y + 65, 120, 8))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 60, self.pos.y + 65, 120 * hpRatio, 8))

class BossRoll:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200)
        self.hp = 14000
        self.maxHp = 14000
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        self.orbitAngle = 0
        self.phase = 1

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        if self.timer < 1125: self.phase = 1
        elif self.timer < 2250: self.phase = 2
        elif self.timer < 3375: self.phase = 3
        else: self.phase = 4

        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.02) * 100
        self.pos.y = 150 + math.cos(self.timer * 0.03) * 50
        self.rect.center = (self.pos.x, self.pos.y)
        self.orbitAngle += 0.05

        if self.phase == 1:
            # [기] 육각성(Hexagram) 펄스
            # 패턴 1: 3중 나선 교차 (시계/반시계 동시 회전)
            if self.timer % 4 == 0:
                for i in range(3):
                    angle1 = self.orbitAngle * 2 + (i * 2 * math.pi / 3)
                    angle2 = -self.orbitAngle * 2 + (i * 2 * math.pi / 3)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle1), math.sin(angle1)) * 5, CYAN, 8, 5))
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle2), math.sin(angle2)) * 5, WHITE, 8, 5))
            # 패턴 2: 주기적인 12방향 확산탄
            if self.timer % 60 == 0:
                for i in range(12):
                    angle = i * (math.pi / 6)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 3, PURPLE, 12, 6))
            # 패턴 3: 빠른 직선 저격탄
            if self.timer % 45 == 0:
                dirVec = (pPos - self.pos).normalize() * 8
                eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, RED, 10, 5))

        elif self.phase == 2:
            # [승] 통제된 회전: 풍차 모양의 거대한 레이저 탄막
            # 패턴 1: 4가닥의 촘촘한 회전 빔 (풍차)
            if self.timer % 3 == 0:
                for i in range(4):
                    angle = self.orbitAngle + (i * math.pi / 2)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 6, GOLD, 10, 5))
            # 패턴 2: 바깥에서 안으로 좁혀오는 역방향 탄막 (압박용)
            if self.timer % 90 == 0:
                for i in range(16):
                    angle = i * (math.pi / 8)
                    spawn_pos = self.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * 400
                    eProjs.append(Projectile(spawn_pos.x, spawn_pos.y, (self.pos - spawn_pos).normalize() * 3, CYAN, 8, 6))
            # 패턴 3: 플레이어 위치를 향한 샷건 
            if self.timer % 70 == 0:
                base_dir = (pPos - self.pos).normalize()
                for a in [-15, -5, 5, 15]:
                    eProjs.append(Projectile(self.pos.x, self.pos.y, base_dir.rotate(a) * 7, RED, 7, 5))

        elif self.phase == 3:
            # [전] 체크보드와 파도: 플레이어의 무빙을 강제하는 체스판 패턴
            # 패턴 1: 상하좌우로 이동하며 쏘는 격자형 탄막
            if self.timer % 15 == 0:
                eProjs.append(Projectile(self.pos.x - 100, self.pos.y, pygame.Vector2(0, 5), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x + 100, self.pos.y, pygame.Vector2(0, 5), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x, self.pos.y - 100, pygame.Vector2(-5, 0), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x, self.pos.y + 100, pygame.Vector2(5, 0), WHITE, 10, 6))
            # 패턴 2: S자 곡선을 그리며 떨어지는 탄막
            if self.timer % 10 == 0:
                wave_x = math.sin(self.timer * 0.1) * 3
                eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(wave_x, 4), PURPLE, 8, 5))
            # 패턴 3: 강력한 양방향 유도탄
            if self.timer % 100 == 0:
                eProjs.append(HomingProjectile(self.pos.x - 50, self.pos.y, pygame.Vector2(-2, 2), CYAN, 15, 8))
                eProjs.append(HomingProjectile(self.pos.x + 50, self.pos.y, pygame.Vector2(2, 2), CYAN, 15, 8))

        elif self.phase == 4:
            # [결] 절대 영도 만다라: 극한의 밀도와 아름다움을 지닌 최종 패턴
            # 패턴 1: 7방향 초고속 회전 나선 (일정 주기마다 회전 방향 반전)
            direction = 1 if (self.timer // 150) % 2 == 0 else -1
            if self.timer % 3 == 0:
                for i in range(7):
                    angle = self.orbitAngle * 3 * direction + (i * 2 * math.pi / 7)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 5, RED, 9, 5))
            # 패턴 2: 조밀하게 팽창하는 링
            if self.timer % 40 == 0:
                for i in range(24):
                    angle = i * (math.pi / 12) + (self.orbitAngle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, GOLD, 10, 6))
            # 패턴 3: 최후의 유도탄 쇄도
            if self.timer % 45 == 0:
                eProjs.append(HomingProjectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), WHITE, 12, 10))

    def draw(self, surf):
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (50, 50, 50), (self.pos.x - 60, self.pos.y + 60, 120, 8))
        pygame.draw.rect(surf, (200, 0, 255), (self.pos.x - 60, self.pos.y + 60, 120 * hpRatio, 8))
        # Zero 코어 이펙트 (회전하는 사각형)
        core_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(core_surf, WHITE, (0,0,40,40), 4)
        rotated_core = pygame.transform.rotate(core_surf, math.degrees(self.orbitAngle * 10))
        surf.blit(rotated_core, rotated_core.get_rect(center=(self.pos.x, self.pos.y)))

