import { useState, useEffect, createContext, useContext } from 'react';
import { api } from '../lib/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [userType, setUserType] = useState(null);
  const [childrenList, setChildrenList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is authenticated on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      setIsLoading(true);
      const response = await api.getCurrentUser();
      setUser(response.user);
      setUserType(response.user_type);
      if (response.children) {
        setChildrenList(response.children);
      }
    } catch (error) {
      console.log('Not authenticated');
      setUser(null);
      setUserType(null);
      setChildrenList([]);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await api.register(userData);
      setUser(response.child);
      setUserType('child');
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const login = async (credentials) => {
    try {
      setError(null);
      const response = await api.login(credentials);
      setUser(response.user);
      setUserType(response.user_type);
      if (response.children) {
        setChildrenList(response.children);
      }
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.logout();
      setUser(null);
      setUserType(null);
      setChildrenList([]);
      setError(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const selectTheme = async (theme) => {
    try {
      setError(null);
      const response = await api.selectTheme(theme);
      setUser(response.user);
      
      // Update document theme
      document.documentElement.setAttribute('data-theme', theme);
      
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const value = {
    user,
    userType,
    children: childrenList,
    isLoading,
    error,
    register,
    login,
    logout,
    selectTheme,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

