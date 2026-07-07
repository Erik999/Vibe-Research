#!/bin/bash
# Vibe-Research 一键启动脚本
# 启动后端 FastAPI (:8900) + 前端 Vite (:5899)

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Vibe-Research 启动中..."
echo "============================================"

# ── 启动后端 ──
echo "[1/2] 启动后端 FastAPI (0.0.0.0:8900)..."
cd "$ROOT_DIR/backend"
if [ ! -d ".venv" ]; then
    echo "  → 创建虚拟环境..."
    python3.11 -m venv .venv
    .venv/bin/pip install -r requirements.txt -q
fi
.venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8900 &
BACKEND_PID=$!
sleep 2

# ── 启动前端 ──
echo "[2/2] 启动前端 Vite (0.0.0.0:5899)..."
cd "$ROOT_DIR/frontend"
npm run dev -- --host 0.0.0.0 --port 5899 &
FRONTEND_PID=$!
sleep 3

echo ""
echo "============================================"
echo "  ✅ 启动完成！"
echo "  后端 API:  http://0.0.0.0:8900/docs"
echo "  前端看板:  http://0.0.0.0:5899"
echo "  后端 PID:  $BACKEND_PID"
echo "  前端 PID:  $FRONTEND_PID"
echo "============================================"
echo ""
echo "  停止服务: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# 保持脚本运行，方便 Ctrl+C 一键终止
wait
