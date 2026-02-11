import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    team_id: ''
  });
  const [saveError, setSaveError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const baseUrl = codespace 
    ? `https://${codespace}-8000.app.github.dev/api`
    : 'http://localhost:8000/api';

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const fetchUsers = async () => {
    try {
      console.log('Fetching users from:', `${baseUrl}/users/`);
      
      const response = await fetch(`${baseUrl}/users/`);
      const data = await response.json();
      
      console.log('Users API Response:', data);
      
      // Handle both paginated (.results) and plain array responses
      const usersData = data.results || data;
      setUsers(Array.isArray(usersData) ? usersData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      console.log('Fetching teams from:', `${baseUrl}/teams/`);
      
      const response = await fetch(`${baseUrl}/teams/`);
      const data = await response.json();
      
      console.log('Teams API Response:', data);
      
      const teamsData = data.results || data;
      setTeams(Array.isArray(teamsData) ? teamsData : []);
    } catch (err) {
      console.error('Error fetching teams:', err);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      username: user.username,
      email: user.email,
      team_id: user.team_id
    });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleCancel = () => {
    setEditingUser(null);
    setFormData({ name: '', username: '', email: '', team_id: '' });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaveError(null);
    setSaveSuccess(false);

    try {
      const response = await fetch(`${baseUrl}/users/${editingUser._id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData));
      }

      const updatedUser = await response.json();
      
      // Update the users list with the updated user
      setUsers(users.map(u => u._id === updatedUser._id ? updatedUser : u));
      setSaveSuccess(true);
      
      // Close the edit form after a short delay
      setTimeout(() => {
        handleCancel();
      }, 1500);
    } catch (err) {
      console.error('Error saving user:', err);
      setSaveError(err.message);
    }
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => t._id === teamId);
    return team ? team.name : teamId;
  };

  if (loading) return <div className="container mt-4"><p>Loading users...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Users (Superheroes)</h2>
      <p className="text-muted">Total heroes: {users.length}</p>

      {editingUser && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Edit User: {editingUser.name}</h5>
            {saveSuccess && (
              <div className="alert alert-success" role="alert">
                User updated successfully!
              </div>
            )}
            {saveError && (
              <div className="alert alert-danger" role="alert">
                Error saving user: {saveError}
              </div>
            )}
            <form onSubmit={handleSave}>
              <div className="row mb-3">
                <div className="col-md-6">
                  <label className="form-label">Name</label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              <div className="row mb-3">
                <div className="col-md-6">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Team</label>
                  <select
                    className="form-select"
                    name="team_id"
                    value={formData.team_id}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select a team</option>
                    {teams.map((team) => (
                      <option key={team._id} value={team._id}>
                        {team.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="d-flex gap-2">
                <button type="submit" className="btn btn-primary">
                  Save Changes
                </button>
                <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-hover table-dark">
          <thead>
            <tr>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Team</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user._id}>
                <td><strong>{user.name}</strong></td>
                <td>@{user.username}</td>
                <td>{user.email}</td>
                <td>{getTeamName(user.team_id)}</td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                  <button 
                    className="btn btn-sm btn-primary"
                    onClick={() => handleEdit(user)}
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Users;
