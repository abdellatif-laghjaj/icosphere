import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Constants for icosahedron
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2
VERTICES = np.array([
    (-1, GOLDEN_RATIO, 0), (1, GOLDEN_RATIO, 0), (-1, -GOLDEN_RATIO, 0), (1, -GOLDEN_RATIO, 0),
    (0, -1, GOLDEN_RATIO), (0, 1, GOLDEN_RATIO), (0, -1, -GOLDEN_RATIO), (0, 1, -GOLDEN_RATIO),
    (GOLDEN_RATIO, 0, -1), (GOLDEN_RATIO, 0, 1), (-GOLDEN_RATIO, 0, -1), (-GOLDEN_RATIO, 0, 1)
])
FACES = np.array([
    (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
    (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
    (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
    (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
])


# Function to convert spherical to cartesian coordinates
def spherical_to_cartesian(lat, lon, r=1):
    x = r * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    y = r * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    z = r * np.sin(np.radians(lat))
    return x, y, z


# Function to create a spherical triangle
def create_spherical_triangle(v1, v2, v3, color='red'):  # Default to red
    # Normalize vertices to unit sphere
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    v3 = v3 / np.linalg.norm(v3)

    # Create arcs between vertices
    arc1 = create_arc(v1, v2)
    arc2 = create_arc(v2, v3)
    arc3 = create_arc(v3, v1)

    # Combine arcs into a single trace
    x = np.concatenate((arc1[:, 0], arc2[:, 0], arc3[:, 0]))
    y = np.concatenate((arc1[:, 1], arc2[:, 1], arc3[:, 1]))
    z = np.concatenate((arc1[:, 2], arc2[:, 2], arc3[:, 2]))

    return go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=color, width=2))


# Function to create a great circle arc between two points
def create_arc(start, end, n=50):
    # Calculate rotation axis and angle
    axis = np.cross(start, end)
    angle = np.arccos(np.dot(start, end))

    # Generate points along the arc
    t = np.linspace(0, angle, n)

    # Pre-allocate array for arc points
    arc = np.zeros((n, 3))

    # Calculate rotation for each point on the arc
    for i in range(n):
        rot_mat = rotation_matrix(axis, t[i])
        arc[i, :] = np.matmul(rot_mat, start[:, np.newaxis]).squeeze()

    return arc


# Function to create a rotation matrix
def rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    a = np.cos(angle)
    b = np.sin(angle)
    c = 1 - a

    return np.array([
        [a + axis[0] ** 2 * c, axis[0] * axis[1] * c - axis[2] * b, axis[0] * axis[2] * c + axis[1] * b],
        [axis[1] * axis[0] * c + axis[2] * b, a + axis[1] ** 2 * c, axis[1] * axis[2] * c - axis[0] * b],
        [axis[2] * axis[0] * c - axis[1] * b, axis[2] * axis[1] * c + axis[0] * b, a + axis[2] ** 2 * c]
    ])


# Function to subdivide a triangle into four smaller triangles
def subdivide_triangle(v1, v2, v3):
    midpoint1 = (v1 + v2) / 2
    midpoint2 = (v2 + v3) / 2
    midpoint3 = (v3 + v1) / 2
    return [
        (v1, midpoint1, midpoint3),
        (midpoint1, v2, midpoint2),
        (midpoint2, v3, midpoint3),
        (midpoint1, midpoint2, midpoint3)
    ]


# Streamlit app
st.title("Interactive Spherical Icosahedron")

# Initialize session state
if 'triangles' not in st.session_state:
    st.session_state.triangles = []
    for i in range(20):
        v1 = VERTICES[FACES[i, 0]]
        v2 = VERTICES[FACES[i, 1]]
        v3 = VERTICES[FACES[i, 2]]
        st.session_state.triangles.append((v1, v2, v3))
    st.session_state.subdivided = set()  # Track subdivided triangles

# Dynamic select dropdown for selecting triangle
triangle_options = list(range(len(st.session_state.triangles)))
selected_triangle_index = st.sidebar.selectbox("Select Triangle Index:", options=triangle_options)
selected_triangle = st.session_state.triangles[selected_triangle_index]

# Subdivide selected triangle
if st.sidebar.button("Subdivide Selected Triangle"):
    subdivided_triangles = subdivide_triangle(*selected_triangle)
    st.session_state.triangles.pop(selected_triangle_index)
    st.session_state.triangles.extend(subdivided_triangles)
    st.session_state.subdivided.add(selected_triangle_index)
    st.session_state.subdivided.update(range(len(st.session_state.triangles) - 4, len(st.session_state.triangles)))

# Create Plotly figure
fig = go.Figure()

# Add sphere
u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=[[0, 'rgb(200,200,200)'], [1, 'rgb(200,200,200)']],
                         showscale=False, opacity=0.3))

# Add icosahedron triangles
for i, triangle in enumerate(st.session_state.triangles):
    if i in st.session_state.subdivided:
        color = 'green'
    elif i == selected_triangle_index:
        color = 'blue'
    else:
        color = 'red'
    fig.add_trace(create_spherical_triangle(*triangle, color=color))

# Update layout
fig.update_layout(
    title_text='Spherical Icosahedron',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='data'
    ),
    height=600,
    width=800
)

# Display figure in Streamlit
st.plotly_chart(fig)

# Display total number of triangles
st.sidebar.write(f"Total number of triangles: {len(st.session_state.triangles)}")
