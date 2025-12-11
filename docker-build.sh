#!/bin/bash
# SOSParser Docker Build Script

set -e

echo "🐳 Building SOSParser Docker Image..."
echo ""

# Build the image
docker build -t sosparser:latest .

echo ""
echo "✅ Build complete!"
echo ""
echo "Image: sosparser:latest"
docker images | grep sosparser
echo ""
echo "To run:"
echo "  docker run -d -p 8000:8000 --name sosparser sosparser:latest"
echo ""
echo "Or use docker-compose:"
echo "  docker-compose up -d"
