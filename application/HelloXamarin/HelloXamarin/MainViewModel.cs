using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Input;
using System.Threading.Tasks;
using Plugin.Media;
using Xamarin.Forms;
using System.Net.Http;
using Plugin.Media.Abstractions;
using Newtonsoft.Json.Linq;
using Xamarin.Essentials;

namespace HelloXamarin
{
    public class MainViewModel : INotify
    {

        public MainViewModel()
        {
            OnRecipe = false;
            RecommendFood = string.Empty;
            //FoodImage = "photo.png";
        }

        private bool _OnRecipe;
        public bool OnRecipe
        {
            get { return _OnRecipe; }
            set { _OnRecipe = value; RaisePropertyChanged("OnRecipe"); }
        }

        private string _RecommendFood;
        public string RecommendFood
        {
            get { return _RecommendFood; }
            set { _RecommendFood = value; RaisePropertyChanged("RecommendFood"); }
        }

        private string _FoodImage;
        public string FoodImage
        {
            get { return _FoodImage; }
            set { _FoodImage = value; RaisePropertyChanged("FoodImage"); }
        }

        private string recipe_url = string.Empty;
        private bool url_ok = false;
        public MediaFile file;
        
        #region OpenCamera
        async void OpenCameraExecute()
        {
            await CrossMedia.Current.Initialize();
            file = await CrossMedia.Current.TakePhotoAsync(new Plugin.Media.Abstractions.StoreCameraMediaOptions
            {
                PhotoSize = Plugin.Media.Abstractions.PhotoSize.Medium,
                Directory = "Sample",
                Name = "test.jpg"
            });
            if (file == null) return;

            //RecommendFood = content.ToString();
            FoodImage = file.Path;
            OnRecipe = true;
            //LoadRecipe();
        }

        bool CanOpenCameraExecute()
        {
            if (!CrossMedia.Current.IsCameraAvailable
               || !CrossMedia.Current.IsTakePhotoSupported)
            {
                return false;
            }
            return true;
        }

        public ICommand OpenCamera { get { return new RelayCommand(OpenCameraExecute, CanOpenCameraExecute); } }
        #endregion

        #region SendPicture

        async void SendPictureExecute()
        {
            var content = new MultipartFormDataContent
            {
                {
                    new StreamContent(file.GetStream()),
                    "\"file\"",
                    $"\"{file.Path}\""
                }
            };

            var httpClient = new HttpClient();
            HttpResponseMessage responseMessage = null;
            try
            {
                var uploadServiceBaseAddress = "http://141.164.49.86:5000/GetRecipe";
                responseMessage = await httpClient.PostAsync(uploadServiceBaseAddress, content);

                //지금은 음식이름만 갖고옴, 추후에 json으로 레시피까지 
                RecommendFood = await responseMessage.Content.ReadAsStringAsync();
                JObject json = JObject.Parse(RecommendFood);
                //var res = await App.Current.MainPage.DisplayAlert(json["success"].ToString(), json["msg"].ToString(), "Ok", "Cancel");
                recipe_url = json["msg"].ToString();
                url_ok = bool.Parse(json["success"].ToString());
                if(url_ok == false)
                {
                    msgbox("onemore time take a picture.");
                } else
                {
                    msgbox("Successfully");
                }
                //msgbox("Successfully receiving data.");
                //그리고 Get Recipe버튼 눌러서 레시피 가지고 오기   
            }
            catch (HttpRequestException e)
            {
                if(responseMessage == null)
                {
                    responseMessage = new HttpResponseMessage();
                }
                msgbox(e.Message);
            }

        }

        bool CanSendPictureExecute()
        {
            return true;
        }

        public ICommand SendPicture { get { return new RelayCommand(SendPictureExecute, CanSendPictureExecute); } }
        #endregion

        async void msgbox(string msg)
        {
            var res = await App.Current.MainPage.DisplayAlert("msg", msg, "Ok", "NO");

        }

        #region GetRecipe
        /*
        public async void OpenBrowser(Uri uri)
        {
            await Browser.OpenAsync(uri, BrowserLaunchType.SystemPreferred);
        }*/

        [Obsolete]
        void GetRecipeExecute()
        {
            if (url_ok == false)
            {
                msgbox("please send picture to server your image file");
            }
            else
            {
                
                Uri uri = new Uri(recipe_url);
                Device.OpenUri(uri);
                //OpenBrowser(uri);
            }
        }

        bool CanGetRecipeExecute()
        {
            return true;
        }

        public ICommand GetRecipe
        { get { return new RelayCommand(GetRecipeExecute, CanGetRecipeExecute);}}
        #endregion

        //var res = await App.Current.MainPage.DisplayAlert("Success", "Your data are saved", "Ok", "Cancel");
    }
}
