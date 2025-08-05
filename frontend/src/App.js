import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ShoppingCart, Plus, Minus, Clock, MapPin, Phone, User, Star, Truck, ChefHat, Package, CheckCircle, ArrowLeft, Menu as MenuIcon, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Cart Context
const CartContext = React.createContext();

// Components
const Header = ({ cartItemsCount, onToggleMenu, showMenu }) => {
  return (
    <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-red-600 to-orange-600 rounded-full flex items-center justify-center">
                <ChefHat className="h-6 w-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gray-900">PizzApp</span>
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-red-600 transition-colors">Inicio</Link>
            <Link to="/menu" className="text-gray-700 hover:text-red-600 transition-colors">Menú</Link>
            <Link to="/track" className="text-gray-700 hover:text-red-600 transition-colors">Seguir Pedido</Link>
            <Link to="/admin" className="text-gray-700 hover:text-red-600 transition-colors">Admin</Link>
          </nav>

          <div className="flex items-center space-x-4">
            <Link to="/cart" className="relative p-2 text-gray-700 hover:text-red-600 transition-colors">
              <ShoppingCart className="h-6 w-6" />
              {cartItemsCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {cartItemsCount}
                </span>
              )}
            </Link>
            
            <button
              onClick={onToggleMenu}
              className="md:hidden p-2 text-gray-700 hover:text-red-600 transition-colors"
            >
              {showMenu ? <X className="h-6 w-6" /> : <MenuIcon className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {showMenu && (
          <div className="md:hidden">
            <div className="bg-white border-t border-gray-200 px-2 pt-2 pb-3 space-y-1">
              <Link to="/" className="block px-3 py-2 text-gray-700 hover:text-red-600 transition-colors">Inicio</Link>
              <Link to="/menu" className="block px-3 py-2 text-gray-700 hover:text-red-600 transition-colors">Menú</Link>
              <Link to="/track" className="block px-3 py-2 text-gray-700 hover:text-red-600 transition-colors">Seguir Pedido</Link>
              <Link to="/admin" className="block px-3 py-2 text-gray-700 hover:text-red-600 transition-colors">Admin</Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-red-600 to-orange-600 rounded-full flex items-center justify-center">
                <ChefHat className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold">PizzApp</span>
            </div>
            <p className="text-gray-400">La mejor pizza de Asunción, ahora al alcance de un click.</p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Contacto</h3>
            <div className="space-y-2 text-gray-400">
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4" />
                <span>(021) 123-456</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4" />
                <span>Asunción, Paraguay</span>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Horarios</h3>
            <div className="space-y-2 text-gray-400">
              <p>Lun - Dom: 18:00 - 23:30</p>
              <p>Delivery hasta medianoche</p>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Zonas de Entrega</h3>
            <div className="space-y-2 text-gray-400">
              <p>• Centro - Gs. 15.000</p>
              <p>• San Lorenzo - Gs. 20.000</p>
              <p>• Lambaré - Gs. 20.000</p>
              <p>• Fernando de la Mora - Gs. 20.000</p>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 PizzApp. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1593504049359-74330189a345?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwzfHxwaXp6YXxlbnwwfHx8fDE3NTQzOTkxNjl8MA&ixlib=rb-4.1.0&q=85')`
          }}
        />
        <div className="absolute inset-0 bg-black/60" />
        
        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            La Mejor Pizza de
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-orange-400">
              Asunción
            </span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-200">
            Delivery rápido, sabores únicos y la experiencia que te mereces
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={() => navigate('/menu')}
              className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300 transform hover:scale-105"
            >
              Ver Menú
            </button>
            <button 
              onClick={() => navigate('/track')}
              className="border-2 border-white text-white hover:bg-white hover:text-gray-900 px-8 py-4 rounded-full text-lg font-semibold transition-all duration-300"
            >
              Seguir Pedido
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">¿Por qué elegirnos?</h2>
            <p className="text-xl text-gray-600">La experiencia perfecta, desde el pedido hasta tu mesa</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-red-50 to-orange-50 hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-red-600 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Clock className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Delivery Rápido</h3>
              <p className="text-gray-600">Entrega garantizada en 45 minutos o menos</p>
            </div>
            
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-red-50 to-orange-50 hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-red-600 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Calidad Premium</h3>
              <p className="text-gray-600">Ingredientes frescos y recetas únicas</p>
            </div>
            
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-red-50 to-orange-50 hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-red-600 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Truck className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Seguimiento en Tiempo Real</h3>
              <p className="text-gray-600">Sigue tu pedido desde la cocina hasta tu puerta</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section 
        className="py-20 relative"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1617347454431-f49d7ff5c3b1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwxfHxmb29kJTIwZGVsaXZlcnl8ZW58MHx8fHwxNzU0Mzg4MzQxfDA&ixlib=rb-4.1.0&q=85')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="absolute inset-0 bg-black/70" />
        <div className="relative z-10 max-w-4xl mx-auto text-center text-white px-4">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">¿Listo para ordenar?</h2>
          <p className="text-xl mb-8">Tu pizza favorita está a solo unos clicks de distancia</p>
          <button 
            onClick={() => navigate('/menu')}
            className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white px-12 py-4 rounded-full text-xl font-semibold transition-all duration-300 transform hover:scale-105"
          >
            Ordenar Ahora
          </button>
        </div>
      </section>
    </div>
  );
};

const Menu = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { addToCart } = React.useContext(CartContext);

  const categories = [
    { id: 'all', name: 'Todos', icon: '🍽️' },
    { id: 'pizzas', name: 'Pizzas', icon: '🍕' },
    { id: 'hamburguesas', name: 'Hamburguesas', icon: '🍔' },
    { id: 'bebidas', name: 'Bebidas', icon: '🥤' },
    { id: 'acompañamientos', name: 'Acompañamientos', icon: '🍟' }
  ];

  useEffect(() => {
    fetchMenu();
  }, []);

  const fetchMenu = async () => {
    try {
      const response = await axios.get(`${API}/menu`);
      setMenuItems(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching menu:', error);
      setLoading(false);
    }
  };

  const filteredItems = selectedCategory === 'all' 
    ? menuItems 
    : menuItems.filter(item => item.category === selectedCategory);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(price);
  };

  if (loading) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Cargando menú...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Nuestro Menú</h1>
          <p className="text-xl text-gray-600">Sabores únicos que te van a enamorar</p>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-6 py-3 rounded-full text-sm font-semibold transition-all duration-300 ${
                selectedCategory === category.id
                  ? 'bg-gradient-to-r from-red-600 to-orange-600 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              <span className="mr-2">{category.icon}</span>
              {category.name}
            </button>
          ))}
        </div>

        {/* Menu Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map(item => (
            <div key={item.id} className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
              <div className="h-48 overflow-hidden">
                <img 
                  src={item.image_url} 
                  alt={item.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{item.name}</h3>
                <p className="text-gray-600 mb-4">{item.description}</p>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-2xl font-bold text-red-600">{formatPrice(item.price)}</span>
                  <div className="flex items-center text-gray-500">
                    <Clock className="h-4 w-4 mr-1" />
                    <span className="text-sm">{item.preparation_time} min</span>
                  </div>
                </div>
                <button
                  onClick={() => addToCart(item)}
                  className="w-full bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105"
                >
                  <Plus className="h-5 w-5 inline mr-2" />
                  Agregar al Carrito
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredItems.length === 0 && (
          <div className="text-center py-16">
            <p className="text-xl text-gray-600">No hay productos disponibles en esta categoría.</p>
          </div>
        )}
      </div>
    </div>
  );
};

const Cart = () => {
  const { cartItems, updateQuantity, removeFromCart, getTotalPrice, clearCart } = React.useContext(CartContext);
  const navigate = useNavigate();

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(price);
  };

  if (cartItems.length === 0) {
    return (
      <div className="pt-16 min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ShoppingCart className="h-24 w-24 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Tu carrito está vacío</h2>
          <p className="text-gray-600 mb-6">¡Agrega algunos productos deliciosos!</p>
          <button
            onClick={() => navigate('/menu')}
            className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white px-8 py-3 rounded-xl font-semibold transition-all duration-300"
          >
            Ver Menú
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-16 min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center mb-8">
          <button
            onClick={() => navigate('/menu')}
            className="mr-4 p-2 text-gray-600 hover:text-red-600 transition-colors"
          >
            <ArrowLeft className="h-6 w-6" />
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Tu Carrito</h1>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          {cartItems.map(item => (
            <div key={item.id} className="flex items-center justify-between py-4 border-b border-gray-200 last:border-b-0">
              <div className="flex items-center">
                <img 
                  src={item.image_url} 
                  alt={item.name}
                  className="w-16 h-16 object-cover rounded-lg mr-4"
                />
                <div>
                  <h3 className="font-semibold text-gray-900">{item.name}</h3>
                  <p className="text-red-600 font-bold">{formatPrice(item.price)}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="p-1 text-gray-500 hover:text-red-600 transition-colors"
                >
                  <Minus className="h-5 w-5" />
                </button>
                <span className="font-semibold text-lg">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="p-1 text-gray-500 hover:text-red-600 transition-colors"
                >
                  <Plus className="h-5 w-5" />
                </button>
                <button
                  onClick={() => removeFromCart(item.id)}
                  className="ml-4 p-1 text-gray-500 hover:text-red-600 transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex justify-between items-center text-xl font-bold text-gray-900 mb-6">
            <span>Total:</span>
            <span className="text-red-600">{formatPrice(getTotalPrice())}</span>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={clearCart}
              className="flex-1 border-2 border-gray-300 text-gray-700 hover:bg-gray-100 py-3 rounded-xl font-semibold transition-all duration-300"
            >
              Vaciar Carrito
            </button>
            <button
              onClick={() => navigate('/checkout')}
              className="flex-1 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white py-3 rounded-xl font-semibold transition-all duration-300"
            >
              Proceder al Pago
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const Checkout = () => {
  const { cartItems, getTotalPrice, clearCart } = React.useContext(CartContext);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_phone: '',
    delivery_address: '',
    delivery_zone: 'centro',
    payment_method: 'cash',
    delivery_notes: ''
  });

  const deliveryZones = [
    { id: 'centro', name: 'Centro', fee: 15000 },
    { id: 'san_lorenzo', name: 'San Lorenzo', fee: 20000 },
    { id: 'lambare', name: 'Lambaré', fee: 20000 },
    { id: 'fernando_mora', name: 'Fernando de la Mora', fee: 20000 }
  ];

  const getCurrentZone = () => deliveryZones.find(zone => zone.id === formData.delivery_zone);
  const subtotal = getTotalPrice();
  const deliveryFee = getCurrentZone()?.fee || 15000;
  const total = subtotal + deliveryFee;

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(price);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const orderData = {
        items: cartItems.map(item => ({
          menu_item_id: item.id,
          quantity: item.quantity,
          special_instructions: ""
        })),
        delivery_info: {
          customer_name: formData.customer_name,
          customer_phone: formData.customer_phone,
          delivery_address: formData.delivery_address,
          delivery_zone: formData.delivery_zone
        },
        payment_method: formData.payment_method,
        delivery_notes: formData.delivery_notes
      };

      const response = await axios.post(`${API}/orders`, orderData);
      clearCart();
      navigate(`/track/${response.data.id}`);
    } catch (error) {
      console.error('Error creating order:', error);
      alert('Error al crear el pedido. Por favor intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  if (cartItems.length === 0) {
    navigate('/cart');
    return null;
  }

  return (
    <div className="pt-16 min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center mb-8">
          <button
            onClick={() => navigate('/cart')}
            className="mr-4 p-2 text-gray-600 hover:text-red-600 transition-colors"
          >
            <ArrowLeft className="h-6 w-6" />
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Finalizar Pedido</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Form */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Información de Entrega</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <User className="h-4 w-4 inline mr-2" />
                  Nombre Completo
                </label>
                <input
                  type="text"
                  required
                  value={formData.customer_name}
                  onChange={(e) => setFormData({...formData, customer_name: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="Tu nombre completo"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Phone className="h-4 w-4 inline mr-2" />
                  Teléfono
                </label>
                <input
                  type="tel"
                  required
                  value={formData.customer_phone}
                  onChange={(e) => setFormData({...formData, customer_phone: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="0981 123 456"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <MapPin className="h-4 w-4 inline mr-2" />
                  Dirección de Entrega
                </label>
                <textarea
                  required
                  value={formData.delivery_address}
                  onChange={(e) => setFormData({...formData, delivery_address: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  rows="3"
                  placeholder="Calle, número, referencias..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Zona de Entrega</label>
                <select
                  value={formData.delivery_zone}
                  onChange={(e) => setFormData({...formData, delivery_zone: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                >
                  {deliveryZones.map(zone => (
                    <option key={zone.id} value={zone.id}>
                      {zone.name} - {formatPrice(zone.fee)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Método de Pago</label>
                <select
                  value={formData.payment_method}
                  onChange={(e) => setFormData({...formData, payment_method: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                >
                  <option value="cash">Efectivo</option>
                  <option value="transfer">Transferencia</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Notas Adicionales</label>
                <textarea
                  value={formData.delivery_notes}
                  onChange={(e) => setFormData({...formData, delivery_notes: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  rows="2"
                  placeholder="Instrucciones especiales..."
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 disabled:opacity-50 text-white py-4 rounded-xl font-semibold transition-all duration-300"
              >
                {loading ? 'Procesando...' : 'Confirmar Pedido'}
              </button>
            </form>
          </div>

          {/* Order Summary */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Resumen del Pedido</h2>
            
            <div className="space-y-4 mb-6">
              {cartItems.map(item => (
                <div key={item.id} className="flex justify-between items-center">
                  <div>
                    <span className="font-medium">{item.name}</span>
                    <span className="text-gray-500 ml-2">x{item.quantity}</span>
                  </div>
                  <span className="font-semibold">{formatPrice(item.price * item.quantity)}</span>
                </div>
              ))}
            </div>
            
            <div className="border-t border-gray-200 pt-4 space-y-2">
              <div className="flex justify-between">
                <span>Subtotal:</span>
                <span>{formatPrice(subtotal)}</span>
              </div>
              <div className="flex justify-between">
                <span>Envío ({getCurrentZone()?.name}):</span>
                <span>{formatPrice(deliveryFee)}</span>
              </div>
              <div className="flex justify-between text-xl font-bold text-red-600 pt-2 border-t border-gray-200">
                <span>Total:</span>
                <span>{formatPrice(total)}</span>
              </div>
            </div>

            <div className="mt-6 p-4 bg-red-50 rounded-xl">
              <div className="flex items-center text-red-800">
                <Clock className="h-5 w-5 mr-2" />
                <span className="font-semibold">Tiempo estimado: 45 minutos</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const TrackOrder = () => {
  const [orderId, setOrderId] = useState('');
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const orderStatuses = {
    'received': { label: 'Recibido', icon: Package, color: 'text-blue-600', bgColor: 'bg-blue-100' },
    'confirmed': { label: 'Confirmado', icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-100' },
    'preparing': { label: 'Preparando', icon: ChefHat, color: 'text-yellow-600', bgColor: 'bg-yellow-100' },
    'ready': { label: 'Listo', icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-100' },
    'on_route': { label: 'En Camino', icon: Truck, color: 'text-purple-600', bgColor: 'bg-purple-100' },
    'delivered': { label: 'Entregado', icon: CheckCircle, color: 'text-green-600', bgColor: 'bg-green-100' },
    'cancelled': { label: 'Cancelado', icon: X, color: 'text-red-600', bgColor: 'bg-red-100' }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(price);
  };

  const searchOrder = async () => {
    if (!orderId.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API}/orders/${orderId}`);
      setOrder(response.data);
    } catch (error) {
      setError('Pedido no encontrado. Verifica el número de pedido.');
      setOrder(null);
    } finally {
      setLoading(false);
    }
  };

  const getStatusInfo = (status) => orderStatuses[status] || orderStatuses['received'];

  return (
    <div className="pt-16 min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Seguir Pedido</h1>
          <p className="text-gray-600">Ingresa el número de tu pedido para ver el estado</p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={orderId}
              onChange={(e) => setOrderId(e.target.value)}
              placeholder="Número de pedido (ej: 123e4567-e89b-12d3...)"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && searchOrder()}
            />
            <button
              onClick={searchOrder}
              disabled={loading}
              className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-semibold transition-all duration-300"
            >
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Order Details */}
        {order && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Pedido #{order.id.substring(0, 8)}</h2>
              <p className="text-gray-600">Cliente: {order.delivery_info.customer_name}</p>
              <p className="text-gray-600">Teléfono: {order.delivery_info.customer_phone}</p>
            </div>

            {/* Status */}
            <div className="mb-8">
              <div className="flex items-center space-x-3 mb-4">
                <div className={`p-3 rounded-full ${getStatusInfo(order.status).bgColor}`}>
                  {React.createElement(getStatusInfo(order.status).icon, {
                    className: `h-6 w-6 ${getStatusInfo(order.status).color}`
                  })}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{getStatusInfo(order.status).label}</h3>
                  <p className="text-gray-600">Estado actual del pedido</p>
                </div>
              </div>

              {/* Status Progress */}
              <div className="flex justify-between items-center mb-4">
                {['received', 'confirmed', 'preparing', 'ready', 'on_route', 'delivered'].map((status, index) => {
                  const isActive = ['received', 'confirmed', 'preparing', 'ready', 'on_route', 'delivered'].indexOf(order.status) >= index;
                  const isCurrent = order.status === status;
                  
                  return (
                    <div key={status} className="flex-1 flex items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                        isCurrent 
                          ? `${getStatusInfo(status).bgColor} ${getStatusInfo(status).color}` 
                          : isActive 
                            ? 'bg-green-100 text-green-600' 
                            : 'bg-gray-100 text-gray-400'
                      }`}>
                        {index + 1}
                      </div>
                      {index < 5 && (
                        <div className={`flex-1 h-1 mx-2 ${
                          isActive ? 'bg-green-600' : 'bg-gray-200'
                        }`} />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Order Items */}
            <div className="mb-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Productos</h3>
              <div className="space-y-3">
                {order.items.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <span className="font-medium">Producto #{item.menu_item_id.substring(0, 8)}</span>
                      <span className="text-gray-500 ml-2">x{item.quantity}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Delivery Info */}
            <div className="mb-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Información de Entrega</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                  <MapPin className="h-5 w-5 text-gray-500 mt-1" />
                  <div>
                    <p className="font-medium text-gray-900">{order.delivery_info.delivery_address}</p>
                    <p className="text-sm text-gray-600">Zona: {order.delivery_info.delivery_zone}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Order Summary */}
            <div className="border-t border-gray-200 pt-4">
              <div className="flex justify-between items-center text-sm text-gray-600 mb-2">
                <span>Subtotal:</span>
                <span>{formatPrice(order.subtotal)}</span>
              </div>
              <div className="flex justify-between items-center text-sm text-gray-600 mb-2">
                <span>Envío:</span>
                <span>{formatPrice(order.delivery_fee)}</span>
              </div>
              <div className="flex justify-between items-center text-lg font-bold text-gray-900">
                <span>Total:</span>
                <span className="text-red-600">{formatPrice(order.total)}</span>
              </div>
            </div>

            {/* Estimated Delivery */}
            <div className="mt-6 p-4 bg-red-50 rounded-xl">
              <div className="flex items-center text-red-800">
                <Clock className="h-5 w-5 mr-2" />
                <span className="font-semibold">
                  Entrega estimada: {new Date(order.estimated_delivery).toLocaleTimeString('es-PY', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const AdminDashboard = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [analytics, setAnalytics] = useState(null);

  const orderStatuses = {
    'received': { label: 'Recibido', color: 'bg-blue-100 text-blue-800' },
    'confirmed': { label: 'Confirmado', color: 'bg-green-100 text-green-800' },
    'preparing': { label: 'Preparando', color: 'bg-yellow-100 text-yellow-800' },
    'ready': { label: 'Listo', color: 'bg-green-100 text-green-800' },
    'on_route': { label: 'En Camino', color: 'bg-purple-100 text-purple-800' },
    'delivered': { label: 'Entregado', color: 'bg-green-100 text-green-800' },
    'cancelled': { label: 'Cancelado', color: 'bg-red-100 text-red-800' }
  };

  useEffect(() => {
    fetchOrders();
    fetchAnalytics();
    // Set up real-time updates (simplified for MVP)
    const interval = setInterval(() => {
      fetchOrders();
      fetchAnalytics();
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API}/orders`);
      setOrders(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching orders:', error);
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/analytics/today`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await axios.put(`${API}/orders/${orderId}/status`, { status: newStatus });
      fetchOrders(); // Refresh orders
    } catch (error) {
      console.error('Error updating order status:', error);
      alert('Error al actualizar el estado del pedido');
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(price);
  };

  const filteredOrders = selectedStatus === 'all' 
    ? orders 
    : orders.filter(order => order.status === selectedStatus);

  if (loading) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-16 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Dashboard Administrativo</h1>
          
          {/* Analytics Cards */}
          {analytics && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-blue-100 rounded-full">
                    <Package className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Pedidos Hoy</h3>
                    <p className="text-3xl font-bold text-blue-600">{analytics.total_orders}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-green-100 rounded-full">
                    <span className="text-2xl">₲</span>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Ventas Hoy</h3>
                    <p className="text-3xl font-bold text-green-600">{formatPrice(analytics.total_revenue)}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-purple-100 rounded-full">
                    <Clock className="h-8 w-8 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">Promedio</h3>
                    <p className="text-3xl font-bold text-purple-600">45min</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Status Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setSelectedStatus('all')}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
              selectedStatus === 'all'
                ? 'bg-gray-900 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            Todos ({orders.length})
          </button>
          
          {Object.entries(orderStatuses).map(([status, config]) => {
            const count = orders.filter(order => order.status === status).length;
            return (
              <button
                key={status}
                onClick={() => setSelectedStatus(status)}
                className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
                  selectedStatus === status
                    ? 'bg-gray-900 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {config.label} ({count})
              </button>
            );
          })}
        </div>

        {/* Orders List */}
        <div className="space-y-4">
          {filteredOrders.map(order => (
            <div key={order.id} className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-4 mb-4">
                    <h3 className="text-xl font-bold text-gray-900">
                      Pedido #{order.id.substring(0, 8)}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${orderStatuses[order.status].color}`}>
                      {orderStatuses[order.status].label}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleTimeString('es-PY', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Cliente</p>
                      <p className="font-semibold">{order.delivery_info.customer_name}</p>
                      <p className="text-sm text-gray-600">{order.delivery_info.customer_phone}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Dirección</p>
                      <p className="font-semibold">{order.delivery_info.delivery_address}</p>
                      <p className="text-sm text-gray-600">Zona: {order.delivery_info.delivery_zone}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">{order.items.length} productos</p>
                      <p className="text-xl font-bold text-red-600">{formatPrice(order.total)}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Método de pago</p>
                      <p className="font-semibold capitalize">{order.payment_method}</p>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 lg:mt-0 lg:ml-6">
                  <div className="flex flex-col space-y-2">
                    {order.status === 'received' && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'confirmed')}
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        Confirmar
                      </button>
                    )}
                    {order.status === 'confirmed' && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'preparing')}
                        className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        Preparando
                      </button>
                    )}
                    {order.status === 'preparing' && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'ready')}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        Listo
                      </button>
                    )}
                    {order.status === 'ready' && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'on_route')}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        En Camino
                      </button>
                    )}
                    {order.status === 'on_route' && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'delivered')}
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        Entregado
                      </button>
                    )}
                    
                    {!['delivered', 'cancelled'].includes(order.status) && (
                      <button
                        onClick={() => updateOrderStatus(order.id, 'cancelled')}
                        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        Cancelar
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredOrders.length === 0 && (
          <div className="text-center py-16">
            <Package className="h-24 w-24 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay pedidos</h3>
            <p className="text-gray-600">
              {selectedStatus === 'all' 
                ? 'No hay pedidos disponibles.' 
                : `No hay pedidos con estado "${orderStatuses[selectedStatus].label}".`
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [cartItems, setCartItems] = useState([]);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  // Initialize sample menu when app loads
  useEffect(() => {
    const initializeMenu = async () => {
      try {
        await axios.post(`${API}/initialize-menu`);
      } catch (error) {
        console.error('Error initializing menu:', error);
      }
    };
    
    initializeMenu();
  }, []);

  const addToCart = (item) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(cartItem => cartItem.id === item.id);
      if (existingItem) {
        return prevItems.map(cartItem =>
          cartItem.id === item.id
            ? { ...cartItem, quantity: cartItem.quantity + 1 }
            : cartItem
        );
      }
      return [...prevItems, { ...item, quantity: 1 }];
    });
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(itemId);
      return;
    }
    setCartItems(prevItems =>
      prevItems.map(item =>
        item.id === itemId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeFromCart = (itemId) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== itemId));
  };

  const clearCart = () => {
    setCartItems([]);
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getTotalItems = () => {
    return cartItems.reduce((total, item) => total + item.quantity, 0);
  };

  const cartContextValue = {
    cartItems,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    getTotalPrice,
    getTotalItems
  };

  return (
    <CartContext.Provider value={cartContextValue}>
      <div className="App">
        <BrowserRouter>
          <Header 
            cartItemsCount={getTotalItems()} 
            onToggleMenu={() => setShowMobileMenu(!showMobileMenu)}
            showMenu={showMobileMenu}
          />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/menu" element={<Menu />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/track" element={<TrackOrder />} />
            <Route path="/track/:id" element={<TrackOrder />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
          <Footer />
        </BrowserRouter>
      </div>
    </CartContext.Provider>
  );
}

export default App;