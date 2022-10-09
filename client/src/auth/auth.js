import decodeJwt from 'jwt-decode';


const baseUrl = 'http://localhost:8081';


class Auth {
  
  login = async ({email, password}) => {
    if (!(email.length > 0)) {
      throw new Error('Email was not provided');
    }
    if (!(password.length > 0)) {
      throw new Error('Password was not provided');
    }
    const formData = new FormData();
    // formData.append('email', email);
    // lolz, make up your mind...
    formData.append('username', email);
    formData.append('password', password);
    const request = new Request(baseUrl + '/auth/login', {
      method: 'POST',
      body: formData,
    });
    const response = await fetch(request);
    if (response.status === 500) {
      throw new Error('Internal server error');
    }
    const data = await response.json();
    console.log("data", data);
    // 400 error handling
    if (response.status >= 400 && response.status < 500) {
      if (data.detail) {
        throw data.detail;
      }
      throw data;
    }
  if ('access_token' in data) {
    // eslint-disable-next-line
    const decodedToken = decodeJwt(data['access_token']);
    console.log("Decoded token", decodedToken)
    localStorage.setItem('token', data['access_token']);
    localStorage.setItem('permissions', 'user');
  } else {
    console.log("Error, no access token");
  }
    return data
  };

  register = async ({email, username, password, passwordConfirmation}) => {
    if (!((username.length) > 0)) {
      throw new Error('Username was not provided');
    }
    if (!((email.length) > 0)) {
      throw new Error('Username was not provided');
    }
    if (!(password.length > 0)) {
      throw new Error('Password was not provided');
    }
    if (!(passwordConfirmation.length > 0)) {
      throw new Error('Password confirmation was not provided');
    }
    if (password !== passwordConfirmation) {
      throw new Error('Passwords do not match');
    }
    const formData = { email, username, password };
    const request = new Request(baseUrl + '/auth/register', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    const response = await fetch(request);
    if (response.status === 500) {
      throw new Error('Internal server error');
    }
    const data = await response.json();
    if (response.status >= 400 && response.status < 500) {
      if (data.detail) {
        throw data.detail;
      }
      throw data;
    }
    if ('access_token' in data) {
      // eslint-disable-next-line
      const decodedToken = decodeJwt(data['access_token']);
      console.log("Decoded token", decodedToken)
      localStorage.setItem('token', data['access_token']);
      localStorage.setItem('permissions', 'user');
    }
    return data;
  };

  logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('permissions');
  };

  getUser = async () => {
    const token = localStorage.getItem('token');
    const request = new Request(baseUrl + '/auth/users/me', {
      method: 'GET',
      headers: {'Authorization': `Bearer ${token}`}
    });
    const response = await fetch(request);
    const data = await response.json();
    return data
  };

  isAuthenticated = () => {
    const permissions = localStorage.getItem('permissions');
    return !!permissions && permissions === 'user';
  };
};

export default new Auth();
