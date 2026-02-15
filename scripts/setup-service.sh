#!/bin/bash
set -e

# ============================================
# EC2 부팅 시 자동 시작 서비스 등록
# EC2에서 1회만 실행하면 됩니다
# ============================================

echo "[1/2] systemd 서비스 생성..."

sudo tee /etc/systemd/system/skydream.service > /dev/null << 'EOF'
[Unit]
Description=Skydream Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ec2-user/skydream
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

echo "[2/2] 서비스 등록..."
sudo systemctl daemon-reload
sudo systemctl enable skydream

echo ""
echo "✅ 완료! EC2가 재부팅되어도 자동으로 서비스가 시작됩니다."
echo "   상태 확인: sudo systemctl status skydream"
