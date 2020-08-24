using Plugin.Media;
using Plugin.Media.Abstractions;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace HelloXamarin
{
    // Learn more about making custom code visible in the Xamarin.Forms previewer
    // by visiting https://aka.ms/xamarinforms-previewer
    [DesignTimeVisible(false)]
    public partial class MainPage : ContentPage, INotifyPropertyChanged
    {
        public MainPage()
        {
            InitializeComponent();
            //this.BindingContext = this;
            this.BindingContext = new MainViewModel();
        }
        /*
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


        private async void takePhoto_Clicked(object sender, EventArgs e)
        {
            await CrossMedia.Current.Initialize();
            MediaFile file;
            if (!CrossMedia.Current.IsCameraAvailable || !CrossMedia.Current.IsTakePhotoSupported)
            {
                await DisplayAlert("No Camera", ":( No camera avaialble.", "OK");
                return;
            }
            try
            {
                //Exception occurs in this code.
                file = await CrossMedia.Current.TakePhotoAsync(new StoreCameraMediaOptions
                {
                    //Specify Store to Album OR Directory, not both
                    Directory = "App_Images",
                    Name = "Test.jpg"

                });
            }
            catch (Exception exception)
            {
                await DisplayAlert("Error", exception.Message, "OK");
                //I've got a break point here which is being hit, but the exception is (null)
                throw;
            }

            if (file == null)
                return;

            RecommendFood = "asda";
        }

        #region INotify
        public event PropertyChangedEventHandler PropertyChanged;

        public void RaisePropertyChanged(string property)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(property));
            }
        }
        #endregion
        */
    }
}
    
