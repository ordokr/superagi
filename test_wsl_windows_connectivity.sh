#!/bin/bash

# Test script to verify WSL to Windows connectivity for SuperAGI

echo "🔍 Testing WSL to Windows connectivity for SuperAGI..."
echo "=================================================="

# Get Windows IP
WINDOWS_IP="192.168.0.144"
echo "🖥️  Windows IP: $WINDOWS_IP"

# Get WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo "🐧 WSL IP: $WSL_IP"

echo ""
echo "🌐 Testing network connectivity..."

# Test ping to Windows
echo "📡 Testing ping to Windows..."
if ping -c 3 $WINDOWS_IP > /dev/null 2>&1; then
    echo "✅ Ping to Windows successful"
else
    echo "❌ Ping to Windows failed"
fi

echo ""
echo "🔌 Testing port connectivity..."

# Test LM Studio port (1234)
echo "🤖 Testing LM Studio port 1234..."
if timeout 5 bash -c "</dev/tcp/$WINDOWS_IP/1234" 2>/dev/null; then
    echo "✅ LM Studio port 1234 is accessible"
else
    echo "❌ LM Studio port 1234 is not accessible"
    echo "   Make sure LM Studio is running and listening on 0.0.0.0:1234"
fi

# Test if SuperAGI would be accessible from Windows
echo "🚀 Testing if SuperAGI port 3000 is accessible from WSL..."
if timeout 5 bash -c "</dev/tcp/localhost/3000" 2>/dev/null; then
    echo "✅ SuperAGI port 3000 is accessible locally"
else
    echo "❌ SuperAGI port 3000 is not accessible locally"
fi

echo ""
echo "🔥 Testing Windows Firewall..."

# Test if Windows allows connections from WSL
echo "🛡️  Testing if Windows firewall allows WSL connections..."
echo "   This test attempts to connect to common Windows services..."

# Test Windows RPC endpoint mapper (port 135) - usually open
if timeout 3 bash -c "</dev/tcp/$WINDOWS_IP/135" 2>/dev/null; then
    echo "✅ Windows is accepting connections from WSL (port 135 accessible)"
else
    echo "⚠️  Windows may be blocking connections from WSL"
    echo "   Run the configure_windows_firewall.ps1 script as Administrator on Windows"
fi

echo ""
echo "📋 Summary and Recommendations:"
echo "================================"

echo "1. 🔧 On Windows, run as Administrator:"
echo "   PowerShell -ExecutionPolicy Bypass -File configure_windows_firewall.ps1"
echo ""
echo "2. 🤖 Make sure LM Studio is running and configured to listen on:"
echo "   - Host: 0.0.0.0 (not 127.0.0.1 or localhost)"
echo "   - Port: 1234"
echo ""
echo "3. 🌐 Access SuperAGI from Windows browser at:"
echo "   http://$WSL_IP:3000"
echo ""
echo "4. 🔗 Configure SuperAGI to use LM Studio at:"
echo "   http://$WINDOWS_IP:1234"

echo ""
echo "🎯 If everything is working, you should see SuperAGI UI instead of 'Initializing SuperAGI'"
