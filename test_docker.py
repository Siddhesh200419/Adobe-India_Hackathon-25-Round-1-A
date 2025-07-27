#!/usr/bin/env python3
"""
Test script to verify Docker setup works correctly
"""

import os
import subprocess
import json
import glob

def test_docker_build():
    """Test if Docker image builds successfully."""
    print("🔨 Testing Docker build...")
    try:
        result = subprocess.run([
            "docker", "build", "--platform", "linux/amd64", 
            "-t", "pdf-outline-extractor:test", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Docker build successful!")
            return True
        else:
            print("❌ Docker build failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Docker build error: {e}")
        return False

def test_docker_run():
    """Test if Docker container runs successfully."""
    print("\n🚀 Testing Docker run...")
    
    # Create test output directory
    os.makedirs("output", exist_ok=True)
    
    try:
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath('input')}:/app/input",
            "-v", f"{os.path.abspath('output')}:/app/output",
            "--network", "none",
            "pdf-outline-extractor:test"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Docker run successful!")
            print("Output:", result.stdout)
            return True
        else:
            print("❌ Docker run failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Docker run error: {e}")
        return False

def check_output_files():
    """Check if output JSON files were generated."""
    print("\n📁 Checking output files...")
    
    pdf_files = glob.glob("input/*.pdf")
    json_files = glob.glob("output/*.json")
    
    print(f"Found {len(pdf_files)} PDF files in input/")
    print(f"Generated {len(json_files)} JSON files in output/")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ {os.path.basename(json_file)}: {data.get('title', 'No title')}")
            print(f"   - {len(data.get('outline', []))} headings found")
            
        except Exception as e:
            print(f"❌ Error reading {json_file}: {e}")
    
    return len(json_files) > 0

def main():
    """Run all tests."""
    print("🧪 Testing PDF Outline Extractor Docker Setup\n")
    
    # Test 1: Docker build
    if not test_docker_build():
        return
    
    # Test 2: Docker run
    if not test_docker_run():
        return
    
    # Test 3: Check output
    if not check_output_files():
        print("❌ No output files generated")
        return
    
    print("\n🎉 All tests passed! Docker setup is working correctly.")

if __name__ == "__main__":
    main() 