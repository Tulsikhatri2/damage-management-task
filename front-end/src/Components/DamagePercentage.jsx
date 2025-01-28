import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Typography, Container, Box, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle } from "@mui/material";

const DamagePercentage = () => {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [image1Preview, setImage1Preview] = useState(null);
  const [image2Preview, setImage2Preview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!image1 || !image2) {
      setError("Please upload both images.");
      return;
    }

    const formData = new FormData();
    formData.append("image1", image1);
    formData.append("image2", image2);

    setLoading(true); // Show loading indicator

    try {
      setError("");
      const response = await axios.post("http://127.0.0.1:5000/compare-images", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data);
      setOpenDialog(true); // Open dialog with results
    } catch (err) {
      setError("An error occurred while comparing images.");
      console.error(err);
    } finally {
      setLoading(false); // Hide loading indicator after request
    }
  };

  // Handle image preview
  const handleImage1Change = (e) => {
    const file = e.target.files[0];
    setImage1(file);
    setImage1Preview(URL.createObjectURL(file)); // Preview image
  };

  const handleImage2Change = (e) => {
    const file = e.target.files[0];
    setImage2(file);
    setImage2Preview(URL.createObjectURL(file)); // Preview image
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };

  return (
    <Container maxWidth="xl" sx={{ padding: "20px" , background: "linear-gradient(to bottom,rgb(195, 182, 225), white)"}}>
      <Box textAlign="center" mb={2}>
        <Typography variant="h4" color="linear-gradient(to right, #0f0c29, #302b63, #24243e)" fontWeight="bold"
        sx={{fontFamily:"inherit"}}>
          Damage Percentage Calculation
        </Typography>
      </Box>
      <Box textAlign="center" mb={2}>
          <Button variant="contained" onClick={handleSubmit} disabled={loading}
          sx={{fontFamily:"inherit", backgroundColor:"rgb(103, 57, 212)"}}>
            Compare
          </Button>
        </Box>
        {loading && <CircularProgress />}

        {error && <Typography sx={{fontFamily:"inherit", color:"maroon", fontWeight:"bold",paddingBottom:"2vh"}} textAlign={"center"}>{error}</Typography>}

      <form noValidate>
        <Box display="flex" justifyContent="center" mb={3}>
          {/* Left Section for Image 1 */}
          <Box flex={1} mr={2} display="flex" flexDirection="column" >
            <TextField
              type="file"
              fullWidth
              variant="outlined"
              onChange={handleImage1Change}
            />
            {image1Preview && (
              <Box mt={2} >
                <img
                  src={image1Preview}
                  alt="Image 1 Preview"
                  style={{
                    width: "100%",
                    height: "90%",
                    objectFit: "contain",
                    display: "block",
                  }}
                />
              </Box>
            )}
          </Box>

          {/* Right Section for Image 2 */}
          <Box flex={1} ml={2} display="flex" flexDirection="column" >
            <TextField
              type="file"
              fullWidth
              variant="outlined"
              onChange={handleImage2Change}
            />
            {image2Preview && (
              <Box mt={2}>
                <img
                  src={image2Preview}
                  alt="Image 2 Preview"
                  style={{
                    width: "100%",
                    height: "90%",
                    objectFit: "contain",
                    display: "block",
                  }}
                />
              </Box>
            )}
          </Box>
        </Box>
      </form>

      {/* Dialog for Results */}
      <Dialog open={openDialog} onClose={handleDialogClose}>
        <DialogTitle sx={{fontFamily:"inherit", textAlign:"center", textDecoration:"underline"}}>Comparison Results</DialogTitle>
        <DialogContent>
          {result ? (
            <>
              <Typography variant="body1" sx={{fontFamily:"inherit",textAlign:"center"}}>Similarity: <span style={{color:"maroon", fontWeight:"bold"}}>{result.similarity}</span></Typography>
              <Typography variant="body1" sx={{fontFamily:"inherit",textAlign:"center"}}>Difference Percentage: <span style={{color:"maroon", fontWeight:"bold"}}>{result.differencePercentage}%</span></Typography>
            </>
          ) : (
            <Typography variant="body1" sx={{fontFamily:"inherit",textAlign:"center"}}>An error occurred while comparing images.</Typography>
          )}
        </DialogContent>
        <DialogActions sx={{display:"flex",alignItems:"center",width:"94%",justifyContent:"center"}} >
          <Button onClick={handleDialogClose} sx={{fontFamily:"inherit", backgroundColor:"rgb(103, 57, 212)",color:"white"}}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DamagePercentage;
