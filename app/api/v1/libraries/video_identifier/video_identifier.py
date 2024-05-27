import cv2
import numpy as np
from sklearn.decomposition import PCA
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(
    "mongodb+srv://admin:ph2pkpzBM8tG2Df3@cluster0.kzpinei.mongodb.net/?retryWrites=true&w=majority"
)
db = client["video_fingerprinting"]["fingerprints"]


# ANSI color codes
class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    END = "\033[0m"


def extract_histograms(video_path, max_frames=None):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if max_frames is not None:
        frame_count = min(frame_count, max_frames)
    histograms = []

    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Compute histogram
        hist = cv2.calcHist([gray_frame], [0], None, [10], [0, 256])
        hist /= np.sum(hist)  # Normalize histogram
        histograms.append(hist.tolist())  # Convert histogram to Python list

    cap.release()

    return histograms


def extract_metadata(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    resolution = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    cap.release()
    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration,
        "resolution": resolution,
    }


def normalize_features(histograms):
    # Convert histograms to array
    features = np.array(histograms)
    # Reshape array to 2D
    features = features.reshape(features.shape[0], -1)
    # Normalize features
    normalized_features = (features - np.mean(features, axis=0)) / np.std(
        features, axis=0
    )
    return normalized_features


def apply_pca(features_video1_normalized, features_video2_normalized):
    # Check the valid range for n_components
    n_components = min(
        features_video1_normalized.shape[0], features_video1_normalized.shape[1]
    )
    # Initialize PCA with the corrected n_components value
    pca = PCA(n_components=n_components)
    # Fit and transform the features of video 1
    features_video1_encoded = pca.fit_transform(features_video1_normalized)
    # Transform the features of video 2 using the same PCA object
    features_video2_encoded = pca.transform(features_video2_normalized)
    return features_video1_encoded, features_video2_encoded


def calculate_similarity(features_video1_encoded, features_video2_encoded):
    # Align the dimensions of the two feature matrices
    min_frames = min(features_video1_encoded.shape[0], features_video2_encoded.shape[0])
    features_video1_encoded = features_video1_encoded[:min_frames]
    features_video2_encoded = features_video2_encoded[:min_frames]

    similarities = np.sum(features_video1_encoded * features_video2_encoded, axis=1) / (
        np.linalg.norm(features_video1_encoded, axis=1)
        * np.linalg.norm(features_video2_encoded, axis=1)
    )
    return np.mean(similarities) * 100


def visualize_matched_frames(video_path1, video_path2, similarity_threshold=0.95):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = cap2.get(cv2.CAP_PROP_FPS)

    matched_frames = []

    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        hist1 = cv2.calcHist([gray_frame1], [0], None, [10], [0, 256])
        hist1 /= np.sum(hist1)
        hist2 = cv2.calcHist([gray_frame2], [0], None, [10], [0, 256])
        hist2 /= np.sum(hist2)

        similarity = np.sum(hist1 * hist2) / np.sqrt(
            np.sum(hist1**2) * np.sum(hist2**2)
        )

        if similarity > similarity_threshold:
            matched_frames.append((frame1, frame2))

    cap1.release()
    cap2.release()

    return matched_frames


# ANSI color codes for metadata and fingerprint
METADATA_COLOR = [Color.CYAN, Color.BLUE, Color.GREEN]
FINGERPRINT_COLOR = [Color.MAGENTA, Color.YELLOW]

# Assuming video_path1 and video_path2 contain the paths to the videos
video_path1 = "video1.mp4"
video_path2 = "video4.mp4"

# Extract metadata from videos
metadata_video1 = extract_metadata(video_path1)
metadata_video2 = extract_metadata(video_path2)

# Extract histograms from videos
histograms_video1 = extract_histograms(video_path1)
histograms_video2 = extract_histograms(video_path2, max_frames=len(histograms_video1))

# Normalize features
features_video1_normalized = normalize_features(histograms_video1)
features_video2_normalized = normalize_features(histograms_video2)

# Apply PCA
features_video1_encoded, features_video2_encoded = apply_pca(
    features_video1_normalized, features_video2_normalized
)

# Calculate similarity
similarity_percentage = calculate_similarity(
    features_video1_encoded, features_video2_encoded
)
print(
    "----------------------------------------------------------------------------------------------------------"
)
print(
    f"{METADATA_COLOR[0]}The similarity between the two videos is approximately: {similarity_percentage:.2f}%{Color.END}"
)
print(
    "----------------------------------------------------------------------------------------------------------"
)
print(
    f"{METADATA_COLOR[1]}Shape of features_video1_encoded: {features_video1_encoded.shape}{Color.END}"
)
print(
    f"{METADATA_COLOR[2]}Shape of features_video2_encoded: {features_video2_encoded.shape}{Color.END}"
)

# Visualize matched frames
matched_frames = visualize_matched_frames(video_path1, video_path2)
print(
    "----------------------------------------------------------------------------------------------------------"
)
print(f"{METADATA_COLOR[0]}Number of matched frames: {len(matched_frames)}{Color.END}")

# Print fingerprints
print(
    "----------------------------------------------------------------------------------------------------------"
)
print(f"{FINGERPRINT_COLOR[0]}Fingerprint of Video 1:{Color.END}")
print(features_video1_encoded)
print()
print(
    "----------------------------------------------------------------------------------------------------------"
)
print(f"{FINGERPRINT_COLOR[1]}Fingerprint of Video 2:{Color.END}")
print(features_video2_encoded)

# Save fingerprints and metadata to MongoDB
original_features_list = features_video1_encoded.tolist()
comparison_features_list = features_video2_encoded.tolist()

# Save fingerprints to MongoDB
# Check if original video data already exists in the database
if db["fingerprints"].count_documents({"video": "original"}) == 0:
    original_fingerprint = {
        "video": "original",
        "metadata": metadata_video1,
        "features": original_features_list,
        "histograms": histograms_video1,
    }
    db["fingerprints"].insert_one(original_fingerprint)
    print("Original video data saved to the database.")
else:
    print("Original video data already exists in the database.")

# Save comparison video data to MongoDB
comparison_video_count = (
    db["fingerprints"].count_documents({"video": {"$regex": "^comparison"}}) + 1
)
comparison_video_name = f"comparison_{comparison_video_count}"
comparison_fingerprint = {
    "video": comparison_video_name,
    "similarity_percentage": similarity_percentage,
    "metadata": metadata_video2,
    "features": comparison_features_list,
    "histograms": histograms_video2,
}
db["fingerprints"].insert_one(comparison_fingerprint)
print(f"Comparison video data saved to the database as '{comparison_video_name}'.")
