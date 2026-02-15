#!/bin/bash
set -e

# ============================================
# skydreamtree.com 배포 스크립트
# ============================================

DOMAIN="skydreamtree.com"
EMAIL="${CERTBOT_EMAIL:-}"

echo "=========================================="
echo "  skydreamtree.com 배포 시작"
echo "=========================================="

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다. 먼저 생성해주세요:"
    echo ""
    echo "cat > .env << 'EOF'"
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
    echo "DB_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
    echo "ADMIN_USERNAME=admin"
    echo "ADMIN_PASSWORD=your-admin-password"
    echo "EOF"
    exit 1
fi

# ============================================
# Step 1: 초기 HTTP 모드로 시작
# ============================================
echo ""
echo "[1/5] HTTP 모드로 초기 시작..."

# 초기 nginx 설정 사용 (SSL 없이)
cp docker/nginx/nginx-init.conf docker/nginx/nginx.conf.bak
cp docker/nginx/nginx-init.conf docker/nginx/nginx-active.conf

# nginx Dockerfile을 임시로 init 설정 사용하도록 수정
cat > docker/nginx/Dockerfile << 'NGINX_DOCKERFILE'
FROM nginx:1.25-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-active.conf /etc/nginx/conf.d/default.conf
EXPOSE 80 443
NGINX_DOCKERFILE

# 빌드 및 실행
docker-compose up -d --build

echo "✅ HTTP 서버 시작 완료"

# ============================================
# Step 2: DB 마이그레이션
# ============================================
echo ""
echo "[2/5] DB 마이그레이션 실행..."
sleep 10  # DB가 완전히 시작될 때까지 대기

docker-compose exec -T web flask db upgrade 2>/dev/null || echo "⚠️  마이그레이션 스킵 (이미 최신이거나 첫 실행)"

echo "✅ DB 마이그레이션 완료"

# ============================================
# Step 3: SSL 인증서 발급
# ============================================
echo ""
echo "[3/5] SSL 인증서 발급..."

if [ -z "$EMAIL" ]; then
    read -p "Let's Encrypt 알림 받을 이메일 주소: " EMAIL
fi

docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email

echo "✅ SSL 인증서 발급 완료"

# ============================================
# Step 4: HTTPS nginx 설정으로 전환
# ============================================
echo ""
echo "[4/5] HTTPS 모드로 전환..."

# HTTPS 설정으로 교체
cp docker/nginx/nginx.conf docker/nginx/nginx-active.conf

# nginx 재빌드 및 재시작
docker-compose up -d --build nginx

echo "✅ HTTPS 설정 적용 완료"

# ============================================
# Step 5: 최종 확인
# ============================================
echo ""
echo "[5/5] 최종 상태 확인..."
docker-compose ps

echo ""
echo "=========================================="
echo "  🎉 배포 완료!"
echo "=========================================="
echo ""
echo "  HTTP:  http://$DOMAIN  (→ HTTPS로 리다이렉트)"
echo "  HTTPS: https://$DOMAIN"
echo "  관리자: https://$DOMAIN/admin"
echo ""
echo "  ⚠️  가비아 DNS에서 A 레코드가 EC2 IP를 가리키는지 확인하세요!"
echo "=========================================="
