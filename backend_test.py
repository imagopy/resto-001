import requests
import sys
import json
from datetime import datetime

class PizzeriaAPITester:
    def __init__(self, base_url="https://4e00d64a-dcf0-47c2-9d77-d801666fd0b0.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_items = []  # Track created items for cleanup

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
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
                    if isinstance(response_data, dict) and 'id' in response_data:
                        print(f"   Created ID: {response_data['id']}")
                    elif isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   Returned {len(response_data)} items")
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

    def test_menu_endpoints(self):
        """Test all menu-related endpoints"""
        print("\n" + "="*50)
        print("TESTING MENU ENDPOINTS")
        print("="*50)
        
        # Initialize sample menu
        success, _ = self.run_test(
            "Initialize Sample Menu",
            "POST",
            "initialize-menu",
            200
        )
        
        # Get all menu items
        success, menu_items = self.run_test(
            "Get All Menu Items",
            "GET", 
            "menu",
            200
        )
        
        if success and menu_items:
            print(f"   Found {len(menu_items)} menu items")
            
            # Test category filtering
            categories = ["pizzas", "hamburguesas", "bebidas", "acompañamientos"]
            for category in categories:
                success, category_items = self.run_test(
                    f"Get Menu by Category - {category}",
                    "GET",
                    f"menu/category/{category}",
                    200
                )
                if success:
                    print(f"   Found {len(category_items)} items in {category}")
            
            # Test creating a new menu item
            new_item_data = {
                "name": "Test Pizza",
                "description": "Pizza de prueba",
                "price": 50000,
                "category": "pizzas",
                "image_url": "https://example.com/test.jpg",
                "available": True,
                "preparation_time": 15
            }
            
            success, created_item = self.run_test(
                "Create New Menu Item",
                "POST",
                "menu",
                200,
                data=new_item_data
            )
            
            if success and created_item:
                item_id = created_item.get('id')
                self.created_items.append(('menu_item', item_id))
                
                # Test updating the menu item
                updated_data = {
                    "name": "Updated Test Pizza",
                    "description": "Pizza de prueba actualizada",
                    "price": 55000,
                    "category": "pizzas",
                    "image_url": "https://example.com/test-updated.jpg",
                    "available": True,
                    "preparation_time": 20
                }
                
                success, _ = self.run_test(
                    "Update Menu Item",
                    "PUT",
                    f"menu/{item_id}",
                    200,
                    data=updated_data
                )
                
                # Test deleting the menu item
                success, _ = self.run_test(
                    "Delete Menu Item",
                    "DELETE",
                    f"menu/{item_id}",
                    200
                )

    def test_order_endpoints(self):
        """Test all order-related endpoints"""
        print("\n" + "="*50)
        print("TESTING ORDER ENDPOINTS")
        print("="*50)
        
        # First get menu items to create a valid order
        success, menu_items = self.run_test(
            "Get Menu Items for Order",
            "GET",
            "menu",
            200
        )
        
        if not success or not menu_items:
            print("❌ Cannot test orders without menu items")
            return
        
        # Create a test order
        order_data = {
            "items": [
                {
                    "menu_item_id": menu_items[0]["id"],
                    "quantity": 2,
                    "special_instructions": "Extra cheese"
                },
                {
                    "menu_item_id": menu_items[1]["id"] if len(menu_items) > 1 else menu_items[0]["id"],
                    "quantity": 1,
                    "special_instructions": ""
                }
            ],
            "delivery_info": {
                "customer_name": "Test Customer",
                "customer_phone": "0981123456",
                "delivery_address": "Test Address 123, Asunción",
                "delivery_zone": "centro"
            },
            "payment_method": "cash",
            "delivery_notes": "Test delivery notes"
        }
        
        success, created_order = self.run_test(
            "Create Order",
            "POST",
            "orders",
            200,
            data=order_data
        )
        
        if success and created_order:
            order_id = created_order.get('id')
            self.created_items.append(('order', order_id))
            
            print(f"   Order Total: {created_order.get('total', 0)} PYG")
            print(f"   Delivery Fee: {created_order.get('delivery_fee', 0)} PYG")
            
            # Test getting all orders
            success, all_orders = self.run_test(
                "Get All Orders",
                "GET",
                "orders",
                200
            )
            
            # Test getting specific order
            success, specific_order = self.run_test(
                "Get Specific Order",
                "GET",
                f"orders/{order_id}",
                200
            )
            
            # Test updating order status
            status_updates = ["confirmed", "preparing", "ready", "on_route", "delivered"]
            for status in status_updates:
                success, _ = self.run_test(
                    f"Update Order Status to {status}",
                    "PUT",
                    f"orders/{order_id}/status",
                    200,
                    data={"status": status}
                )
            
            # Test getting orders by status
            success, delivered_orders = self.run_test(
                "Get Orders by Status - delivered",
                "GET",
                "orders/status/delivered",
                200
            )
            
            # Test creating order with different delivery zone
            order_data_san_lorenzo = order_data.copy()
            order_data_san_lorenzo["delivery_info"]["delivery_zone"] = "san_lorenzo"
            
            success, order_san_lorenzo = self.run_test(
                "Create Order - San Lorenzo Zone",
                "POST",
                "orders",
                200,
                data=order_data_san_lorenzo
            )
            
            if success and order_san_lorenzo:
                print(f"   San Lorenzo Delivery Fee: {order_san_lorenzo.get('delivery_fee', 0)} PYG")
                self.created_items.append(('order', order_san_lorenzo.get('id')))

    def test_delivery_person_endpoints(self):
        """Test delivery person management endpoints"""
        print("\n" + "="*50)
        print("TESTING DELIVERY PERSON ENDPOINTS")
        print("="*50)
        
        # Create delivery person
        delivery_person_data = {
            "name": "Test Delivery Person",
            "phone": "0981654321"
        }
        
        success, created_person = self.run_test(
            "Create Delivery Person",
            "POST",
            "delivery-persons",
            200,
            data=delivery_person_data
        )
        
        if success and created_person:
            person_id = created_person.get('id')
            self.created_items.append(('delivery_person', person_id))
            
            # Get all delivery persons
            success, all_persons = self.run_test(
                "Get All Delivery Persons",
                "GET",
                "delivery-persons",
                200
            )
            
            # Get available delivery persons
            success, available_persons = self.run_test(
                "Get Available Delivery Persons",
                "GET",
                "delivery-persons/available",
                200
            )

    def test_analytics_endpoints(self):
        """Test analytics endpoints"""
        print("\n" + "="*50)
        print("TESTING ANALYTICS ENDPOINTS")
        print("="*50)
        
        success, analytics = self.run_test(
            "Get Today's Analytics",
            "GET",
            "analytics/today",
            200
        )
        
        if success and analytics:
            print(f"   Total Orders Today: {analytics.get('total_orders', 0)}")
            print(f"   Total Revenue Today: {analytics.get('total_revenue', 0)} PYG")
            print(f"   Orders by Status: {analytics.get('orders_by_status', {})}")

    def test_error_cases(self):
        """Test error handling"""
        print("\n" + "="*50)
        print("TESTING ERROR CASES")
        print("="*50)
        
        # Test getting non-existent order
        success, _ = self.run_test(
            "Get Non-existent Order",
            "GET",
            "orders/non-existent-id",
            404
        )
        
        # Test creating order with invalid data
        invalid_order_data = {
            "items": [],  # Empty items should cause error
            "delivery_info": {
                "customer_name": "",  # Empty name
                "customer_phone": "",
                "delivery_address": "",
                "delivery_zone": "centro"
            }
        }
        
        # This might return 422 or 400 depending on validation
        success, _ = self.run_test(
            "Create Order with Invalid Data",
            "POST",
            "orders",
            422  # Expecting validation error
        )
        
        if not success:
            # Try with 400 if 422 didn't work
            success, _ = self.run_test(
                "Create Order with Invalid Data (400)",
                "POST",
                "orders",
                400,
                data=invalid_order_data
            )

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Pizzeria API Tests")
        print(f"Base URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        
        try:
            self.test_menu_endpoints()
            self.test_order_endpoints()
            self.test_delivery_person_endpoints()
            self.test_analytics_endpoints()
            self.test_error_cases()
            
        except Exception as e:
            print(f"\n❌ Test suite failed with error: {str(e)}")
        
        # Print final results
        print("\n" + "="*50)
        print("TEST RESULTS SUMMARY")
        print("="*50)
        print(f"📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    tester = PizzeriaAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())