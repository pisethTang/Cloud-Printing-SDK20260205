#!/usr/bin/env python3
"""
Detailed check of all routes
"""

import demo_app

def check_all_routes():
    """Check detailed information of all routes"""
    print("🔍 Checking route configuration in detail...")
    
    api_routes = []
    other_routes = []
    
    for route in demo_app.app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = list(route.methods) if route.methods else []
            if any(m in ['GET', 'POST', 'PUT', 'DELETE'] for m in methods):
                route_info = (methods, route.path)
                
                if route.path.startswith('/fastapi'):
                    api_routes.append(route_info)
                else:
                    other_routes.append(route_info)
    
    print("📋 API routes (with /fastapi prefix):")
    for methods, path in api_routes:
        method_str = ', '.join([m for m in methods if m not in ['HEAD', 'OPTIONS']])
        print(f"  {method_str:8} {path}")
    
    print("\n📋 Other routes:")
    for methods, path in other_routes:
        method_str = ', '.join([m for m in methods if m not in ['HEAD', 'OPTIONS']])
        print(f"  {method_str:8} {path}")
    
    print(f"\n📊 Statistics:")
    print(f"  Number of API routes: {len(api_routes)}")
    print(f"  Number of other routes: {len(other_routes)}")
    
    expected_api_routes = [
        "/fastapi/",
        "/fastapi/info", 
        "/fastapi/query",
        "/fastapi/result",
        "/fastapi/add_print_job",
        "/fastapi/printer_status/{printer_id}"
    ]
    
    actual_paths = [path for _, path in api_routes]
    
    print(f"\n✅ Expected API routes:")
    for path in expected_api_routes:
        status = "✅" if path in actual_paths else "❌"
        print(f"  {status} {path}")

if __name__ == "__main__":
    check_all_routes()
