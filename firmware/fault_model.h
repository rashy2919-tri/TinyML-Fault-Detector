


    // !!! This file is generated using emlearn !!!

    #include <stdint.h>
    

static inline int32_t fault_detection_model_tree_0(const int16_t *features, int32_t features_length) {
          if (features[0] < 10) {
              return 1;
          } else {
              if (features[4] < 0) {
                  return 2;
              } else {
                  if (features[2] < 194898) {
                      return 3;
                  } else {
                      return 0;
                  }
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_1(const int16_t *features, int32_t features_length) {
          if (features[3] < 2) {
              if (features[0] < 12) {
                  return 1;
              } else {
                  return 2;
              }
          } else {
              if (features[3] < 21) {
                  return 0;
              } else {
                  return 3;
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_2(const int16_t *features, int32_t features_length) {
          if (features[0] < 10) {
              return 1;
          } else {
              if (features[4] < 0) {
                  return 2;
              } else {
                  if (features[0] < 30) {
                      return 0;
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_3(const int16_t *features, int32_t features_length) {
          if (features[0] < 10) {
              return 1;
          } else {
              if (features[0] < 13) {
                  return 0;
              } else {
                  if (features[3] < 20) {
                      return 2;
                  } else {
                      return 3;
                  }
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_4(const int16_t *features, int32_t features_length) {
          if (features[2] < 194069) {
              if (features[1] < 18) {
                  return 1;
              } else {
                  if (features[2] < 32028) {
                      return 2;
                  } else {
                      return 3;
                  }
              }
          } else {
              return 0;
          }
        }
        

static inline int32_t fault_detection_model_tree_5(const int16_t *features, int32_t features_length) {
          if (features[0] < 10) {
              return 1;
          } else {
              if (features[3] < 2) {
                  return 2;
              } else {
                  if (features[4] < 5) {
                      return 3;
                  } else {
                      return 0;
                  }
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_6(const int16_t *features, int32_t features_length) {
          if (features[1] < 59) {
              if (features[0] < 13) {
                  if (features[0] < 10) {
                      return 1;
                  } else {
                      return 0;
                  }
              } else {
                  return 2;
              }
          } else {
              return 3;
          }
        }
        

static inline int32_t fault_detection_model_tree_7(const int16_t *features, int32_t features_length) {
          if (features[0] < 10) {
              return 1;
          } else {
              if (features[2] < 32029) {
                  return 2;
              } else {
                  if (features[4] < 5) {
                      return 3;
                  } else {
                      return 0;
                  }
              }
          }
        }
        

static inline int32_t fault_detection_model_tree_8(const int16_t *features, int32_t features_length) {
          if (features[2] < 194176) {
              if (features[1] < 60) {
                  if (features[1] < 18) {
                      return 1;
                  } else {
                      return 2;
                  }
              } else {
                  return 3;
              }
          } else {
              return 0;
          }
        }
        

static inline int32_t fault_detection_model_tree_9(const int16_t *features, int32_t features_length) {
          if (features[0] < 13) {
              if (features[1] < 22) {
                  return 1;
              } else {
                  return 0;
              }
          } else {
              if (features[2] < 30773) {
                  return 2;
              } else {
                  return 3;
              }
          }
        }
        

int32_t fault_detection_model_predict(const int16_t *features, int32_t features_length) {

        int32_t votes[4] = {0,};
        int32_t _class = -1;

        _class = fault_detection_model_tree_0(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_1(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_2(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_3(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_4(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_5(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_6(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_7(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_8(features, features_length); votes[_class] += 1;
    _class = fault_detection_model_tree_9(features, features_length); votes[_class] += 1;
    
        int32_t most_voted_class = -1;
        int32_t most_voted_votes = 0;
        for (int32_t i=0; i<4; i++) {

            if (votes[i] > most_voted_votes) {
                most_voted_class = i;
                most_voted_votes = votes[i];
            }
        }
        return most_voted_class;
    }
    

int fault_detection_model_predict_proba(const int16_t *features, int32_t features_length, float *out, int out_length) {

        int32_t _class = -1;

        for (int i=0; i<out_length; i++) {
            out[i] = 0.0f;
        }

        _class = fault_detection_model_tree_0(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_1(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_2(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_3(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_4(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_5(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_6(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_7(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_8(features, features_length); out[_class] += 1.0f;
    _class = fault_detection_model_tree_9(features, features_length); out[_class] += 1.0f;
    
        // compute mean
        for (int i=0; i<out_length; i++) {
            out[i] = out[i] / 10;
        }
        return 0;
    }
    