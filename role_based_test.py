import requests
import sys
import json
from datetime import datetime

class RoleBasedAuthTester:
    def __init__(self, base_url="https://4e00d64a-dcf0-47c2-9d77-d801666fd0b0.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.tokens = {}  # Store tokens for each role
        self.test_order_id = None
        
        # Test credentials as specified in the request
        self.test_users = {
            'admin': {'username': 'admin', 'password': 'admin123'},
            'manager': {'username': 'manager', 'password': 'manager123'},
            'kitchen': {'username': 'kitchen', 'password': 'kitchen123'},
            'delivery': {'username': 'delivery', 'password': 'delivery123'}
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None, role=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        # Add auth token if role is specified
        if role and role in self.tokens:
            headers['Authorization'] = f'Bearer {self.tokens[role]}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        if role:
            print(f"   Role: {role}")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    return success, response_data
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_user_creation(self):
        """Test creating default users"""
        print("\n" + "="*60)
        print("TESTING USER CREATION & INITIALIZATION")
        print("="*60)
        
        # Initialize default users
        success, response = self.run_test(
            "Initialize Default Users",
            "POST",
            "auth/init-admin",
            200
        )
        
        if success:
            print(f"   Created users: {response.get('created_users', [])}")
            print(f"   Existing users: {response.get('existing_users', [])}")
        
        return success

    def test_login_for_all_roles(self):
        """Test login for each role"""
        print("\n" + "="*60)
        print("TESTING LOGIN FOR ALL ROLES")
        print("="*60)
        
        all_login_success = True
        
        for role, credentials in self.test_users.items():
            success, response = self.run_test(
                f"Login as {role}",
                "POST",
                "auth/login",
                200,
                data=credentials
            )
            
            if success and 'access_token' in response:
                self.tokens[role] = response['access_token']
                print(f"   ✅ {role} login successful - Token stored")
                
                # Test getting user info
                success, user_info = self.run_test(
                    f"Get {role} user info",
                    "GET",
                    "auth/me",
                    200,
                    role=role
                )
                
                if success:
                    print(f"   User: {user_info.get('username')}, Role: {user_info.get('role')}")
                    
            else:
                all_login_success = False
                print(f"   ❌ {role} login failed")
        
        return all_login_success

    def test_role_based_order_access(self):
        """Test role-based order filtering"""
        print("\n" + "="*60)
        print("TESTING ROLE-BASED ORDER ACCESS")
        print("="*60)
        
        # First create a test order (public endpoint)
        order_data = {
            "items": [
                {
                    "menu_item_id": "test-item-id",
                    "quantity": 2,
                    "special_instructions": "Test order for role testing"
                }
            ],
            "delivery_info": {
                "customer_name": "Role Test Customer",
                "customer_phone": "0981123456",
                "delivery_address": "Test Address 123, Asunción",
                "delivery_zone": "centro"
            },
            "payment_method": "cash",
            "delivery_notes": "Role-based test order"
        }
        
        # Get menu items first to create valid order
        success, menu_items = self.run_test(
            "Get menu items for order creation",
            "GET",
            "menu",
            200
        )
        
        if success and menu_items:
            order_data["items"][0]["menu_item_id"] = menu_items[0]["id"]
            
            success, created_order = self.run_test(
                "Create test order for role testing",
                "POST",
                "orders",
                200,
                data=order_data
            )
            
            if success:
                self.test_order_id = created_order.get('id')
                print(f"   Created test order: {self.test_order_id}")
        
        # Test order access for each role
        for role in ['admin', 'manager', 'kitchen', 'delivery']:
            if role in self.tokens:
                success, orders = self.run_test(
                    f"Get orders as {role}",
                    "GET",
                    "orders",
                    200,
                    role=role
                )
                
                if success:
                    print(f"   {role} can see {len(orders)} orders")
                    
                    # Check if role sees appropriate orders based on status
                    if role == 'kitchen':
                        kitchen_statuses = ['received', 'confirmed', 'preparing', 'ready']
                        visible_orders = [o for o in orders if o['status'] in kitchen_statuses]
                        print(f"   Kitchen should see orders with statuses: {kitchen_statuses}")
                        print(f"   Kitchen sees {len(visible_orders)} relevant orders")
                        
                    elif role == 'delivery':
                        delivery_statuses = ['ready', 'on_route', 'delivered']
                        visible_orders = [o for o in orders if o['status'] in delivery_statuses]
                        print(f"   Delivery should see orders with statuses: {delivery_statuses}")
                        print(f"   Delivery sees {len(visible_orders)} relevant orders")

    def test_role_based_status_updates(self):
        """Test role-based order status update restrictions"""
        print("\n" + "="*60)
        print("TESTING ROLE-BASED STATUS UPDATE RESTRICTIONS")
        print("="*60)
        
        if not self.test_order_id:
            print("❌ No test order available for status update testing")
            return False
        
        # Test Kitchen role restrictions
        print("\n--- Testing Kitchen Role Restrictions ---")
        
        # Kitchen should be able to: received -> confirmed -> preparing -> ready
        kitchen_transitions = [
            ('received', 'confirmed'),
            ('confirmed', 'preparing'), 
            ('preparing', 'ready')
        ]
        
        # Reset order to received status first (as admin)
        if 'admin' in self.tokens:
            self.run_test(
                "Reset order to received (admin)",
                "PUT",
                f"orders/{self.test_order_id}/status",
                200,
                data={"status": "received"},
                role='admin'
            )
        
        # Test valid kitchen transitions
        for current_status, next_status in kitchen_transitions:
            if 'kitchen' in self.tokens:
                success, _ = self.run_test(
                    f"Kitchen: {current_status} -> {next_status}",
                    "PUT",
                    f"orders/{self.test_order_id}/status",
                    200,
                    data={"status": next_status},
                    role='kitchen'
                )
        
        # Test invalid kitchen transition (ready -> on_route should fail)
        if 'kitchen' in self.tokens:
            success, _ = self.run_test(
                "Kitchen: ready -> on_route (should fail)",
                "PUT",
                f"orders/{self.test_order_id}/status",
                403,  # Should be forbidden
                data={"status": "on_route"},
                role='kitchen'
            )
        
        # Test Delivery role restrictions
        print("\n--- Testing Delivery Role Restrictions ---")
        
        # Set order to ready status first (as admin)
        if 'admin' in self.tokens:
            self.run_test(
                "Set order to ready (admin)",
                "PUT",
                f"orders/{self.test_order_id}/status",
                200,
                data={"status": "ready"},
                role='admin'
            )
        
        # Delivery should be able to: ready -> on_route -> delivered
        delivery_transitions = [
            ('ready', 'on_route'),
            ('on_route', 'delivered')
        ]
        
        for current_status, next_status in delivery_transitions:
            if 'delivery' in self.tokens:
                success, _ = self.run_test(
                    f"Delivery: {current_status} -> {next_status}",
                    "PUT",
                    f"orders/{self.test_order_id}/status",
                    200,
                    data={"status": next_status},
                    role='delivery'
                )
        
        # Test invalid delivery transition (should fail for kitchen statuses)
        if 'delivery' in self.tokens:
            # Reset to received first
            if 'admin' in self.tokens:
                self.run_test(
                    "Reset to received for delivery test",
                    "PUT",
                    f"orders/{self.test_order_id}/status",
                    200,
                    data={"status": "received"},
                    role='admin'
                )
            
            success, _ = self.run_test(
                "Delivery: received -> confirmed (should fail)",
                "PUT",
                f"orders/{self.test_order_id}/status",
                403,  # Should be forbidden
                data={"status": "confirmed"},
                role='delivery'
            )

    def test_analytics_access(self):
        """Test analytics access by role"""
        print("\n" + "="*60)
        print("TESTING ANALYTICS ACCESS BY ROLE")
        print("="*60)
        
        # Admin and Manager should have access
        for role in ['admin', 'manager']:
            if role in self.tokens:
                success, analytics = self.run_test(
                    f"Get analytics as {role}",
                    "GET",
                    "analytics/today",
                    200,
                    role=role
                )
                
                if success:
                    print(f"   {role} analytics access: ✅")
                    print(f"   Total orders: {analytics.get('total_orders', 0)}")
                    print(f"   Total revenue: {analytics.get('total_revenue', 0)}")
        
        # Kitchen and Delivery should NOT have access
        for role in ['kitchen', 'delivery']:
            if role in self.tokens:
                success, _ = self.run_test(
                    f"Get analytics as {role} (should fail)",
                    "GET",
                    "analytics/today",
                    403,  # Should be forbidden
                    role=role
                )
                
                if success:
                    print(f"   {role} analytics access: ❌ (correctly denied)")

    def test_user_management_access(self):
        """Test user management access (Admin only)"""
        print("\n" + "="*60)
        print("TESTING USER MANAGEMENT ACCESS (ADMIN ONLY)")
        print("="*60)
        
        # Admin should have access
        if 'admin' in self.tokens:
            success, users = self.run_test(
                "Get all users as admin",
                "GET",
                "users",
                200,
                role='admin'
            )
            
            if success:
                print(f"   Admin can see {len(users)} users")
                for user in users:
                    print(f"   - {user.get('username')} ({user.get('role')})")
        
        # Test creating a new user as admin
        if 'admin' in self.tokens:
            new_user_data = {
                "username": "test_user",
                "email": "test@example.com",
                "password": "testpass123",
                "role": "kitchen"
            }
            
            success, _ = self.run_test(
                "Create new user as admin",
                "POST",
                "users",
                200,
                data=new_user_data,
                role='admin'
            )
        
        # Other roles should NOT have access
        for role in ['manager', 'kitchen', 'delivery']:
            if role in self.tokens:
                success, _ = self.run_test(
                    f"Get users as {role} (should fail)",
                    "GET",
                    "users",
                    403,  # Should be forbidden
                    role=role
                )
                
                if success:
                    print(f"   {role} user management access: ❌ (correctly denied)")

    def test_menu_management_access(self):
        """Test menu management access (Admin/Manager only)"""
        print("\n" + "="*60)
        print("TESTING MENU MANAGEMENT ACCESS")
        print("="*60)
        
        test_menu_item = {
            "name": "Role Test Pizza",
            "description": "Pizza for role testing",
            "price": 60000,
            "category": "pizzas",
            "image_url": "https://example.com/test.jpg",
            "available": True,
            "preparation_time": 15
        }
        
        # Admin and Manager should be able to create menu items
        for role in ['admin', 'manager']:
            if role in self.tokens:
                success, created_item = self.run_test(
                    f"Create menu item as {role}",
                    "POST",
                    "menu",
                    200,
                    data=test_menu_item,
                    role=role
                )
                
                if success:
                    print(f"   {role} can create menu items: ✅")
                    item_id = created_item.get('id')
                    
                    # Test updating the item
                    updated_item = test_menu_item.copy()
                    updated_item['name'] = f"Updated by {role}"
                    
                    success, _ = self.run_test(
                        f"Update menu item as {role}",
                        "PUT",
                        f"menu/{item_id}",
                        200,
                        data=updated_item,
                        role=role
                    )
                    
                    # Test deleting the item
                    success, _ = self.run_test(
                        f"Delete menu item as {role}",
                        "DELETE",
                        f"menu/{item_id}",
                        200,
                        role=role
                    )
        
        # Kitchen and Delivery should NOT be able to manage menu
        for role in ['kitchen', 'delivery']:
            if role in self.tokens:
                success, _ = self.run_test(
                    f"Create menu item as {role} (should fail)",
                    "POST",
                    "menu",
                    403,  # Should be forbidden
                    data=test_menu_item,
                    role=role
                )
                
                if success:
                    print(f"   {role} menu management access: ❌ (correctly denied)")

    def run_all_tests(self):
        """Run all role-based authentication tests"""
        print("🚀 Starting Role-Based Authentication Tests")
        print(f"Base URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        
        try:
            # Initialize sample menu first
            self.run_test("Initialize sample menu", "POST", "initialize-menu", 200)
            
            # Test user creation and login
            if not self.test_user_creation():
                print("❌ User creation failed, stopping tests")
                return 1
            
            if not self.test_login_for_all_roles():
                print("❌ Login tests failed, stopping tests")
                return 1
            
            # Test role-based functionality
            self.test_role_based_order_access()
            self.test_role_based_status_updates()
            self.test_analytics_access()
            self.test_user_management_access()
            self.test_menu_management_access()
            
        except Exception as e:
            print(f"\n❌ Test suite failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Print final results
        print("\n" + "="*60)
        print("ROLE-BASED AUTHENTICATION TEST RESULTS")
        print("="*60)
        print(f"📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All role-based authentication tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            
            # Print summary of what works and what doesn't
            print("\n📋 SUMMARY:")
            print("✅ Working features:")
            print("   - User creation and initialization")
            print("   - Login system for all roles")
            print("   - Basic API access")
            
            print("\n❌ Issues found:")
            print("   - Some role-based restrictions may not be working")
            print("   - Check backend logs for detailed error information")
            
            return 1

def main():
    tester = RoleBasedAuthTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())